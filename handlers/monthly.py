from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery
)

from keyboards.inline_keyboards import (
    monthly_report_keyboard,
    back_to_main_page
)

router = Router()



@router.message(
    F.text == "Oylik hisobotlar"
)
async def monthly_report_menu(
    message: Message
):

    await message.answer(
        "Hisobot turini tanlang:",
        reply_markup=
        monthly_report_keyboard()
    )


from services.monthly_report_service import (
    get_owner_monthly_report
)


@router.callback_query(
    F.data == "monthly_owners"
)
async def monthly_owner_report(
    callback: CallbackQuery
):

    owner_stats, total_profit = (
        await get_owner_monthly_report()
    )

    text = (
        "👤 Oxirgi 30 kun\n\n"
    )

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



from services.monthly_report_service import (
    get_account_monthly_report
)


@router.callback_query(
    F.data == "monthly_accounts"
)
async def monthly_account_report(
    callback: CallbackQuery
):

    account_stats, total_profit = (
        await get_account_monthly_report()
    )

    text = (
        "🎮 Oxirgi 30 kun\n\n"
    )

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