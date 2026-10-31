from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logic.geometry import calculate_geometry
from logic.materials import estimate_materials

router = Router()

class CalcStates(StatesGroup):
    width = State()
    length = State()
    height = State()
    loft = State()
    insulation = State()

@router.callback_query(F.data == "calc_start")
async def calc_start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(CalcStates.width)
    await call.message.edit_text("Введи ширину дома (м, 2–15):")
    await call.answer()

@router.message(CalcStates.width)
async def get_width(message: Message, state: FSMContext):
    try:
        v = float(message.text.replace(",", "."))
        assert 2 <= v <= 15
    except Exception:
        await message.answer("Число от 2 до 15:")
        return
    await state.update_data(width=v)
    await state.set_state(CalcStates.length)
    await message.answer("Длина дома (м, 2–30):")

@router.message(CalcStates.length)
async def get_length(message: Message, state: FSMContext):
    try:
        v = float(message.text.replace(",", "."))
        assert 2 <= v <= 30
    except Exception:
        await message.answer("Число от 2 до 30:")
        return
    await state.update_data(length=v)
    await state.set_state(CalcStates.height)
    await message.answer("Высота до конька (м, 1.5–10):")

@router.message(CalcStates.height)
async def get_height(message: Message, state: FSMContext):
    try:
        v = float(message.text.replace(",", "."))
        assert 1.5 <= v <= 10
    except Exception:
        await message.answer("Число от 1.5 до 10:")
        return
    await state.update_data(height=v)
    await state.set_state(CalcStates.loft)
    await message.answer("Высота антресоли (м, 1.5–4):")

@router.message(CalcStates.loft)
async def get_loft(message: Message, state: FSMContext):
    try:
        v = float(message.text.replace(",", "."))
        assert 1.5 <= v <= 4
    except Exception:
        await message.answer("Число от 1.5 до 4:")
        return
    data = await state.get_data()
    if v >= data["height"]:
        await message.answer("Антресоль не может быть выше конька. Введи заново:")
        return
    await state.update_data(loft=v)
    await state.set_state(CalcStates.insulation)
    await message.answer("Толщина утепления (мм, 150–250):")

@router.message(CalcStates.insulation)
async def get_insulation(message: Message, state: FSMContext):
    try:
        v = float(message.text.replace(",", "."))
        assert 50 <= v <= 400
    except Exception:
        await message.answer("Число от 50 до 400:")
        return
    data = await state.get_data()
    await state.clear()
    geo = calculate_geometry(data["width"], data["length"], data["height"], data["loft"])
    mat = estimate_materials(geo, v)
    text = f"📐 <b>Геометрия</b>\nУклон: {geo['angle_deg']:.1f}°\nСтропила: {geo['rafter_length']:.2f} м\nПлощадь: {geo['floor_area']:.1f} м²\nКровля: {geo['roof_area']:.1f} м²\n\n🧱 <b>Материалы</b>\n"
    for name, val in mat.items():
        text += f"• {name}: {val}\n"
    kb = InlineKeyboardBuilder()
    kb.button(text="🔁 Пересчитать", callback_data="calc_start")
    kb.button(text="🏠 В меню", callback_data="menu")
    kb.adjust(1)
    await message.answer(text, reply_markup=kb.as_markup(), parse_mode="HTML")