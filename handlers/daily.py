from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery
)

from keyboards.inline_keyboards import (
    daily_report_keyboard,
    back_to_main_page
)

router = Router()


@router.message(
    F.text == "Kunlik hisobotlar"
)
async def daily_report_menu(
    message: Message
):

    await message.answer(
        "Hisobot turini tanlang:",
        reply_markup=
        daily_report_keyboard()
    )


from services.daily_report_service import (
    get_owner_daily_report
)


@router.callback_query(
    F.data == "daily_owners"
)
async def daily_owner_report(
    callback: CallbackQuery
):

    owner_stats, total_profit = (
        await get_owner_daily_report()
    )

    text = (
        "👤 Oxirgi 24 soat\n\n"
    )

    if not owner_stats:
        text += "Hisobotlar topilmadi.\n"

    for owner, profit in (
        owner_stats.items()
    ):

        text += (
            f"{owner} : "
            f"{profit:,} so'm\n"
        )

    text += (
        f"\n💰 Umumiy foyda:\n"
        f"{total_profit:,} so'm"
    )

    await callback.message.answer(
        text,
        reply_markup= back_to_main_page()
    )


from services.daily_report_service import (
    get_account_daily_report
)


@router.callback_query(
    F.data == "daily_accounts"
)
async def daily_account_report(
    callback: CallbackQuery
):

    account_stats, total_profit = (
        await get_account_daily_report()
    )

    text = (
        "🎮 Oxirgi 24 soat\n\n"
    )

    if not account_stats:
        text += "Hisobotlar topilmadi.\n"

    for account, profit in (
        account_stats.items()
    ):

        text += (
            f"Akkount {account}"
            f" : "
            f"{profit:,} so'm\n"
        )

    text += (
        f"\n💰 Umumiy tushum:\n"
        f"{total_profit:,} so'm"
    )

    await callback.message.answer(
        text,
        reply_markup= back_to_main_page()
    )