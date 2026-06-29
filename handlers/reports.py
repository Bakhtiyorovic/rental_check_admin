from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from states.hisobot import ReportStates
from keyboards.inline_keyboards import report_accounts_keyboard, night_tariff_keyboard
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

router = Router()

from services.report_service import (
    create_report
)


@router.message(F.text == "Hisobotlar")
async def reports_menu(
    message: Message,
    state: FSMContext
):

    await state.clear()

    await state.set_state(
        ReportStates.waiting_account
    )

    await message.answer(
        "Akkount tanlang:",
        reply_markup=
        await report_accounts_keyboard()
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


@router.callback_query(
    ReportStates.waiting_account,
    F.data.startswith("report_acc_")
)
async def select_account(
    callback: CallbackQuery,
    state: FSMContext
):
    account_number = int(
        callback.data.split("_")[-1]
    )

    await state.update_data(
        account_number=account_number
    )

    await state.set_state(
        ReportStates.waiting_hours
    )

    await callback.message.answer(
        "Necha soatga berildi?",
        reply_markup=night_tariff_keyboard()
    )

    await callback.answer()


@router.callback_query(
    ReportStates.waiting_hours,
    F.data == "night_tariff"
)
async def night_tariff_handler(
    callback: CallbackQuery,
    state: FSMContext
):

    tz = ZoneInfo("Asia/Tashkent")
    now = datetime.now(tz)

    if now.hour < 9:

        target = now.replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0
        )

    else:

        target = (
            now + timedelta(days=1)
        ).replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0
        )

    hours = int(
        round(
            (
                    target - now
            ).total_seconds() / 3600
        )
    )

    await state.update_data(
        hours=hours
    )

    await state.set_state(
        ReportStates.waiting_price
    )

    await callback.message.answer(
        f"🌙 Tungi tarif tanlandi\n"
        f"Soat: {hours}\n\n"
        f"Umumiy summani kiriting:"
    )

    await callback.answer()