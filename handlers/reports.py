from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from states.hisobot import ReportStates
from keyboards.inline_keyboards import report_accounts_keyboard
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command

router = Router()

from services.report_service import (
    create_report
)


@router.message(F.text == "Hisobotlar")
async def reports_menu(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        ReportStates.waiting_account
    )

    await message.answer(
        "Akkount tanlang:",
        reply_markup= await report_accounts_keyboard()
    )


@router.message(
    ReportStates.waiting_hours
)
async def get_hours(
    message: Message,
    state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "Soatni son bilan kiriting."
        )
        return

    await state.update_data(
        hours=int(message.text)
    )

    await state.set_state(
        ReportStates.waiting_price
    )

    await message.answer(
        "Umumiy summani kiriting:"
    )


@router.message(
    ReportStates.waiting_price
)
async def get_price(
    message: Message,
    state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "Summani son bilan kiriting."
        )
        return

    total_price = int(
        message.text
    )

    data = await state.get_data()

    account_number = data[
        "account_number"
    ]

    hours = data["hours"]

    shares = await create_report(
        account_number=account_number,
        hours=hours,
        total_price=total_price
    )

    text = (
        f"Akkount {account_number}\n"
        f"{hours} soatga\n"
        f"umumiy "
        f"{total_price:,} so'mga "
        f"berildi\n\n"
    )

    text += "\n".join(shares)

    await message.answer(text)

    await state.clear()