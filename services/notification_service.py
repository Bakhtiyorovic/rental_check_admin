from aiogram import Bot
from config import INVESTOR_BOT_TOKEN

investor_bot = Bot(
    token=INVESTOR_BOT_TOKEN
)

async def send_report(
    telegram_id: int,
    text: str
):
    try:

        await investor_bot.send_message(
            chat_id=telegram_id,
            text=text
        )

    except Exception as e:

        print(
            f"Send error: {e}"
        )