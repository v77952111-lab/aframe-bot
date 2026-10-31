import json
from pathlib import Path
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
CHECKLIST_FILE = Path(__file__).parent.parent / "data" / "checklists.json"

def _load():
    with open(CHECKLIST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@router.callback_query(F.data == "checklist_menu")
async def checklist_menu(call: CallbackQuery):
    data = _load()
    kb = InlineKeyboardBuilder()
    for key, item in data.items():
        kb.button(text=item["title"], callback_data=f"checklist_{key}")
    kb.button(text="🏠 В меню", callback_data="menu")
    kb.adjust(1)
    await call.message.edit_text("Выбери этап:", reply_markup=kb.as_markup())
    await call.answer()

@router.callback_query(F.data.startswith("checklist_"))
async def checklist_show(call: CallbackQuery):
    key = call.data.replace("checklist_", "", 1)
    data = _load()
    if key not in data:
        await call.answer("Не найдено")
        return
        
    item = data[key]
    steps_text = "\n".join(f"• {s}" for s in item["steps"])
    text = f"<b>{item['title']}</b>\n\n" + steps_text
    
    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ К этапам", callback_data="checklist_menu")
    kb.button(text="🏠 В меню", callback_data="menu")
    kb.adjust(1)
    await call.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await call.answer()