from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 Рассчитать A-frame", callback_data="calc_start")
    kb.button(text="📋 Чек-лист стройки", callback_data="checklist_menu")
    kb.button(text="📊 Анализ акций", callback_data="finance_start")
    kb.button(text="🤖 Спросить ИИ", callback_data="ai_start")
    kb.button(text="ℹ️ Помощь", callback_data="help")
    kb.adjust(1)
    return kb.as_markup()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Я помогу с проектом A-frame дома.\n\nВыбери действие:", reply_markup=main_menu())

@router.callback_query(F.data == "menu")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Главное меню:", reply_markup=main_menu())
    await call.answer()

@router.callback_query(F.data == "help")
async def help_cb(call: CallbackQuery):
    await call.message.edit_text(
        "Что умею:\n"
        "🏠 Рассчитать — площадь, объём, материалы\n"
        "📋 Чек-лист — этапы стройки\n"
        "🤖 ИИ — свободные вопросы по проекту\n\n"
        "/start — вернуться в меню",
    )
    await call.answer()
    from aiogram.filters import Command

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено. Возвращаю в меню.", reply_markup=main_menu())

@router.message(F.text.lower() == "отмена")
async def text_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено. Возвращаю в меню.", reply_markup=main_menu())
