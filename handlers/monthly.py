from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline_keyboards import (
    monthly_report_keyboard,
    back_to_main_page
)

from services.monthly_report_service import (
    get_owner_monthly_report,
    get_account_monthly_report,
    clear_owner_shares
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
        reply_markup=monthly_report_keyboard()
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

    text = "👤 Oxirgi 30 kun\n\n"

    if not owner_stats:
        text += "Hisobotlar topilmadi.\n"

    for owner_name, data in owner_stats.items():

        text += (
            f"{owner_name} : "
            f"{data['profit']:,} so'm\n"
        )

    text += (
        f"\n💰 Umumiy foyda:\n"
        f"{total_profit:,} so'm"
    )

    # Har bir owner uchun "tozalash" tugmasi
    kb = InlineKeyboardBuilder()

    for owner_name, data in owner_stats.items():

        kb.button(
            text=f"🗑 {owner_name} hisobini tozalash",
            callback_data=f"clear_owner_{data['id']}"
        )

    kb.button(
        text="🔙 Asosiy sahifaga qaytish",
        callback_data="cmd_start"
    )

    kb.adjust(1)

    await callback.message.answer(
        text,
        reply_markup=kb.as_markup()
    )


@router.callback_query(
    F.data.startswith("clear_owner_")
)
async def clear_owner_report(
    callback: CallbackQuery
):

    owner_id = int(
        callback.data.split("_")[-1]
    )

    await clear_owner_shares(owner_id)

    await callback.answer(
        "✅ Hisob tozalandi!",
        show_alert=True
    )

    # Yangilangan hisobotni ko'rsatish
    owner_stats, total_profit = (
        await get_owner_monthly_report()
    )

    text = "👤 Oxirgi 30 kun\n\n"

    if not owner_stats:
        text += "Hisobotlar topilmadi.\n"

    for owner_name, data in owner_stats.items():

        text += (
            f"{owner_name} : "
            f"{data['profit']:,} so'm\n"
        )

    text += (
        f"\n💰 Umumiy foyda:\n"
        f"{total_profit:,} so'm"
    )

    kb = InlineKeyboardBuilder()

    for owner_name, data in owner_stats.items():

        kb.button(
            text=f"🗑 {owner_name} hisobini tozalash",
            callback_data=f"clear_owner_{data['id']}"
        )

    kb.button(
        text="🔙 Asosiy sahifaga qaytish",
        callback_data="cmd_start"
    )

    kb.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=kb.as_markup()
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

    text = "🎮 Oxirgi 30 kun\n\n"

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
        reply_markup=back_to_main_page()
    )