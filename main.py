import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from data.config import BOT_TOKEN
from handlers import client, admin


async def main():
    bot = Bot(token=BOT_TOKEN)  # если депрекейт — можно оставить так
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(client.router)
    dp.include_router(admin.router)

    print('Starting polling...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
