import asyncio
from aiogram import Dispatcher

from _bot import bot
from routers import main_router

dp = Dispatcher()


async def main():
    dp.include_router(router=main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
