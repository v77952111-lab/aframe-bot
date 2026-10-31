import asyncio
from aiogram import Bot, Dispatcher 
from aiogram.fsm.storage.memory import MemoryStorage 
from config import BOT_TOKEN 
from handlers import start, calculator, checklist, ai_chat, finance
async def main():
 bot = Bot(token=BOT_TOKEN)
 dp = Dispatcher(storage=MemoryStorage())
 dp.include_router(start.router)
 dp.include_router(calculator.router)
 dp.include_router(checklist.router)
 dp.include_router(ai_chat.router)
 dp.include_router(finance.router)
 print("Бот запущен! Идем в Telegram и проверяем...")
 await dp.start_polling(bot)

if __name__ == "__main__":
 asyncio.run(main())