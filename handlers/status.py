from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards.inline_keyboards import status_keyboard
from states.hisobot import ReportStates

from datetime import datetime
from utils.status_text import (
    generate_status_text
)

from services.account_service import (
    set_account_free,
    get_account_by_number
)


router = Router()

@router.message(F.text == "Akkount statuslar")
async def account_status(message: Message, state: FSMContext):
    text = await generate_status_text()
    await message.answer(
        text,
        reply_markup= await status_keyboard()
    )


@router.callback_query(
    F.data == "status_refresh"
)
async def refresh_status(
    callback: CallbackQuery
):
    await callback.message.edit_text(
        text = await generate_status_text(),
        reply_markup= await status_keyboard()
    )


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

    account = await get_account_by_number(
        account_number
    )

    if not account:

        await callback.answer(
            "Akkount topilmadi",
            show_alert=True
        )
        return

    if account.status == "busy":

        await callback.answer(
            "Bu akkount band",
            show_alert=True
        )
        return

    await state.update_data(
        account_number=account_number
    )

    await state.set_state(
        ReportStates.waiting_hours
    )

    await callback.message.answer(
        "Necha soatga berildi?"
    )

@router.callback_query(
    F.data.startswith("free_")
)
async def free_account(
    callback: CallbackQuery
):

    account_number = int(
        callback.data.split("_")[1]
    )

    success = await set_account_free(
        account_number
    )

    if not success:

        await callback.answer(
            "Akkount topilmadi",
            show_alert=True
        )
        return

    text = await generate_status_text()

    await callback.message.edit_text(
        text,
        reply_markup=
        await status_keyboard()
    )

    await callback.answer(
        "Akkount bo'shatildi"
    )