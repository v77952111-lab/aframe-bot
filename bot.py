import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import start, calculator, checklist, ai_chat, finance

async def health_check(request):
    return web.Response(text="OK")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер запущен на порту {port}")

async def main():
    await start_web_server()
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
