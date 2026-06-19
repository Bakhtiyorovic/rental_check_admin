import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import accounts, reports, start, status, monthly, daily  # handler modulini import
from database.init_db import init_db
from services.monthly_report_service import delete_old_reports
from services.account_service import free_expired_accounts

# Loglarni ko'rish uchun (debug paytida foydali)
logging.basicConfig(level=logging.INFO)


async def account_watcher():

    while True:

        await free_expired_accounts()

        await asyncio.sleep(60)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerni dp'ga biriktirish
    dp.include_router(accounts.router)
    dp.include_router(monthly.router)
    dp.include_router(daily.router)
    dp.include_router(reports.router)
    dp.include_router(start.router)
    dp.include_router(status.router)

    # Eski updatelarni o'chirib yangilarini olish
    await bot.delete_webhook(drop_pending_updates=True)


    await init_db()

    await delete_old_reports()

    asyncio.create_task(
        account_watcher()
    )

    # Botni polling rejimida ishga tushirish
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())