from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from openai import AsyncOpenAI
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

router = Router()

class AIStates(StatesGroup):
    chatting = State()

SYSTEM_PROMPT = "Ты универсальный ИИ-помощник. Ты отлично разбираешься в строительстве A-frame домов, а также в финансовом анализе и инвестициях в акции (США, Израиль, IT-сектор). Отвечай кратко и по делу на русском языке. Если речь идет об инвестициях, всегда добавляй предупреждение, что это не индивидуальная инвестиционная рекомендация."
_client = AsyncOpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL) if LLM_API_KEY else None

@router.callback_query(F.data == "ai_start")
async def ai_start(call: CallbackQuery, state: FSMContext):
    if _client is None:
        await call.message.edit_text("ИИ не подключён. Добавь LLM_API_KEY в .env.")
        await call.answer()
        return
    await state.set_state(AIStates.chatting)
    await state.update_data(history=[{"role": "system", "content": SYSTEM_PROMPT}])
    await call.message.edit_text("🤖 Задай вопрос. /exit — выйти.")
    await call.answer()

@router.message(AIStates.chatting, F.text == "/exit")
async def ai_exit(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вышел. /start — меню.")

@router.message(AIStates.chatting)
async def ai_message(message: Message, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [{"role": "system", "content": SYSTEM_PROMPT}])
    history.append({"role": "user", "content": message.text})
    
    try:
        resp = await _client.chat.completions.create(
            model=LLM_MODEL, 
            messages=history, 
            temperature=0.5
        )
        answer = resp.choices[0].message.content
    except Exception as e:
        await message.answer(f"Ошибка ИИ: {e}")
        return
        
    history.append({"role": "assistant", "content": answer})
    await state.update_data(history=history[-20:])
    await message.answer(answer)