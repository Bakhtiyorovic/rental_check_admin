from datetime import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.account_service import get_free_accounts, get_all_accounts, generate_accounts_text


def accounts_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Akkount qo'shish", callback_data="add_account")
    kb.button(text="➖ Akkount o'chirish", callback_data="delete_account")
    kb.button(text="🔙 Asosiy sahifaga qaytish", callback_data="cmd_start")
    kb.adjust(1)
    return kb.as_markup()


def accounts_list_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Akkount qo'shish", callback_data="add_account")
    kb.button(text="➖ Akkount o'chirish", callback_data="delete_account")
    kb.adjust(1)
    return kb.as_markup()


async def report_accounts_keyboard():
    kb = InlineKeyboardBuilder()
    accounts = await get_free_accounts()

    for account in accounts:
        kb.button(
            text=f"Akkount {account.account_number}",
            callback_data=f"report_acc_{account.account_number}"
        )

    kb.button(text="🔙 Asosiy sahifaga qaytish", callback_data="cmd_start")
    kb.adjust(1)
    return kb.as_markup()


def back_to_main_page():
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Asosiy sahifaga qaytish', callback_data="cmd_start")
    kb.adjust(1)
    return kb.as_markup()


async def status_keyboard():
    kb = InlineKeyboardBuilder()
    accounts = await get_all_accounts()
    now = datetime.utcnow()

    for account in accounts:
        # Faqat statusi busy VA vaqti hali tugamagan akkountlar uchun bekor qilish tugmasi chiqadi
        if account.status == "busy" and account.busy_until and account.busy_until > now:
            kb.button(
                text=f"❌ {account.account_number} bekor",
                callback_data=f"cancel_{account.account_number}"
            )

    kb.button(text="🔙 Asosiy sahifaga qaytish", callback_data="cmd_start")
    kb.adjust(2)
    return kb.as_markup()


def monthly_report_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="👤 Egalar bo'yicha", callback_data="monthly_owners")
    kb.button(text="🎮 Akkountlar bo'yicha", callback_data="monthly_accounts")
    kb.button(text="🔙 Asosiy sahifaga qaytish", callback_data="cmd_start")
    kb.adjust(1)
    return kb.as_markup()


def daily_report_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="👤 Egalar bo'yicha", callback_data="daily_owners")
    kb.button(text="🎮 Akkountlar bo'yicha", callback_data="daily_accounts")
    kb.button(text="🔙 Asosiy sahifaga qaytish", callback_data="cmd_start")
    kb.adjust(1)
    return kb.as_markup()


def night_tariff_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🌙 Tungi tarif", callback_data="night_tariff")
    return kb.as_markup()