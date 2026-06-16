import asyncio
import logging
from aiogram import Bot
from aiogram import Dispatcher

from config import INVESTOR_BOT_TOKEN

from investor_handlers import (
    start,
    reports
)

bot = Bot(
    INVESTOR_BOT_TOKEN
)

dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(reports.router)


async def investor_main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(investor_main())