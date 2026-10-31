from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import yfinance as yf

router = Router()

class FinanceStates(StatesGroup):
    waiting_for_ticker = State()

@router.callback_query(F.data == "finance_start")
async def finance_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(FinanceStates.waiting_for_ticker)
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 В меню", callback_data="menu")
    await call.message.edit_text(
        "Введи тикер акции (например: NVDA, MSFT, MNDY):", 
        reply_markup=kb.as_markup()
    )
    await call.answer()

@router.message(FinanceStates.waiting_for_ticker)
async def process_ticker(message: Message, state: FSMContext):
    ticker = message.text.strip().upper()
    msg = await message.answer(f"⏳ Загружаю данные по {ticker}...")
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        
        if hist.empty:
            await msg.edit_text(f"❌ Не удалось найти данные по тикеру {ticker}.")
            await state.clear()
            return

        current_price = hist['Close'].iloc[-1]
        high_52w = hist['High'].max()
        low_52w = hist['Low'].min()
        start_price = hist['Close'].iloc[0]
        year_change = ((current_price - start_price) / start_price) * 100
        
        text = (
            f"📊 <b>Анализ акции: {ticker}</b>\n\n"
            f"💵 Текущая цена: <b>${current_price:.2f}</b>\n"
            f"📈 Максимум за год: ${high_52w:.2f}\n"
            f"📉 Минимум за год: ${low_52w:.2f}\n\n"
            f"📅 Изменение за год: <b>{year_change:+.2f}%</b>\n\n"
            f"<i>(Данные Yahoo Finance)</i>"
        )
        
        kb = InlineKeyboardBuilder()
        kb.button(text="🔍 Другая акция", callback_data="finance_start")
        kb.button(text="🏠 В меню", callback_data="menu")
        kb.adjust(1)
        
        await msg.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
        await state.clear()
    except Exception as e:
        await msg.edit_text(f"⚠️ Ошибка: {e}")
        await state.clear()