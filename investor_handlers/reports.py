from aiogram import Router
from aiogram.filters import Command

from aiogram.types import Message

from services.investor_service import (
    get_my_reports
)

router = Router()


@router.message(
    Command("reports")
)
async def my_reports(
    message: Message
):

    text = await get_my_reports(
        message.from_user.id
    )

    await message.answer(text)



from sqlalchemy import select



