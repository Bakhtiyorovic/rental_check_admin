from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.account_service import *
#akkount
def accounts_menu():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="➕ Akkount qo'shish",
        callback_data="add_account"
    )

    kb.button(
        text="➖ Akkount o'chirish",
        callback_data="delete_account"
    )

    kb.button(
        text="🔙 Asosiy sahifaga qaytish",
        callback_data="cmd_start"
    )

    kb.adjust(1)

    return kb.as_markup()


def accounts_list_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="➕ Akkount qo'shish",
        callback_data="add_account"
    )

    kb.button(
        text="➖ Akkount o'chirish",
        callback_data="delete_account"
    )

    kb.adjust(1)

    return kb.as_markup()


def generate_accounts_text():

    if not accounts:
        return "Akkountlar mavjud emas"

    text = ""

    for acc_num, data in sorted(accounts.items()):

        text += f"Akkount {acc_num}\n"

        for owner in data["owners"]:

            if owner["name"].lower() == "admin":
                text += f"{owner['name']} {owner['percent']}%\n"

            else:
                text += (
                    f"{owner['name']} "
                    f"({owner['secret_id']}) "
                    f"{owner['percent']}%\n"
                )

        text += "\n"

    return text


#hisobot
async def report_accounts_keyboard():

    kb = InlineKeyboardBuilder()

    accounts = await get_free_accounts()

    for account in accounts:

        kb.button(
            text=f"Akkount {account.account_number}",
            callback_data=(
                f"report_acc_"
                f"{account.account_number}"
            )
        )

    kb.button(
        text="🔙 Asosiy sahifaga qaytish",
        callback_data="cmd_start"
    )

    kb.adjust(1)

    return kb.as_markup()


# def status_keyboard():
#     kb = InlineKeyboardBuilder()
#
#     kb.button(
#         text="🔄 Yangilash",
#         callback_data="status_refresh"
#     )
#
#     return kb.as_markup()



def generate_status_text():

    if not accounts:
        return "Akkountlar mavjud emas."

    text = "🎮 Akkount statuslari\n\n"

    for account_number, data in sorted(accounts.items()):

        if data["status"] == "free":
            emoji = "🟢"
            status = "Bo'sh"

        else:
            emoji = "🔴"
            status = "Band"

        text += (
            f"{emoji} Akkount {account_number}"
            f" | {status}\n"
        )

    kb.button(
        text="🔙 Asosiy sahifaga qaytish",
        callback_data="cmd_start"
    )

    return text


def back_to_main_page():
    kb = InlineKeyboardBuilder()
    kb.button(
        text='🔙 Asosiy sahifaga qaytish',
        callback_data="cmd_start"
    )
    kb.adjust(1)
    return kb.as_markup()


async def status_keyboard():

    kb = InlineKeyboardBuilder()

    accounts = await get_all_accounts()

    # for account in accounts:
    #
    #     if account.status == "busy":
    #
    #         kb.button(
    #             text=(
    #                 f"🔓 "
    #                 f"{account.account_number}"
    #             ),
    #             callback_data=(
    #                 f"free_"
    #                 f"{account.account_number}"
    #             )
    #         )

    kb.button(
        text="🔙 Asosiy sahifaga qaytish",
        callback_data="cmd_start"
    )

    kb.adjust(1)

    return kb.as_markup()


def monthly_report_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="👤 Egalar bo'yicha",
        callback_data="monthly_owners"
    )

    kb.button(
        text="🎮 Akkountlar bo'yicha",
        callback_data="monthly_accounts"
    )

    kb.button(
        text="🔙 Asosiy sahifaga qaytish",
        callback_data="cmd_start"
    )

    kb.adjust(1)

    return kb.as_markup()



def night_tariff_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🌙 Tungi tarif",
        callback_data="night_tariff"
    )

    return kb.as_markup()