from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, reply_keyboard_markup
from states.akkountlar import AddAccountStates, DeleteAccountStates
from keyboards.inline_keyboards import accounts_menu, accounts_list_keyboard, generate_accounts_text, back_to_main_page
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import random
from states.akkountlar import (
    AddAccountStates,
    DeleteAccountStates
)

from services.account_service import (
    account_exists,
    create_account,
    delete_account,
    generate_accounts_text
)


router = Router()

@router.message(F.text == "Akkountlar")
async def accounts_menu_handler(
    message: Message
):
    text = await generate_accounts_text()

    await message.answer(
        text,
        reply_markup=accounts_menu()
    )


# #Akkountlar menyusi
# @router.callback_query(F.data == "accounts")
# async def accounts_menu_handler(callback: CallbackQuery):
#
#     text = generate_accounts_text()
#
#     await callback.message.edit_text(
#         text,
#         reply_markup=accounts_menu()
#     )

#Boshlanish
@router.callback_query(
    F.data == "add_account"
)
async def add_account(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        AddAccountStates.waiting_account_number
    )

    await callback.message.answer(
        "Akkount raqamini kiriting:"
    )

#Raqam qabul qilish
@router.message(
    AddAccountStates.waiting_account_number
)
async def account_number_handler(
    message: Message,
    state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "Faqat son kiriting."
        )
        return

    number = int(message.text)

    exists = await account_exists(
        number
    )

    if exists:

        await message.answer(
            "Bu akkount mavjud."
        )
        return

    await state.update_data(
        account_number=number
    )

    await state.set_state(
        AddAccountStates.waiting_owners
    )

    await message.answer(
        "Egalarni kiriting:\n"
        "admin,sardor,feruz"
    )

#Egalarni qabul qilish
@router.message(
    AddAccountStates.waiting_owners
)
async def owners_handler(
    message: Message,
    state: FSMContext
):

    owners = [
        i.strip()
        for i in message.text.split(",")
        if i.strip()
    ]

    owner_data = []

    for owner in owners:

        if owner.lower() == "admin":

            owner_data.append(
                {
                    "name": owner,
                    "secret_id": None
                }
            )

        else:

            owner_data.append(
                {
                    "name": owner,
                    "secret_id":
                    random.randint(
                        1000,
                        9999
                    )
                }
            )

    await state.update_data(
        owners=owner_data,
        current_index=0,
        percents=[]
    )

    await state.set_state(
        AddAccountStates.waiting_owner_percent
    )

    await message.answer(
        f"{owner_data[0]['name']} uchun foiz:"
    )

#Foizlarni yig'ish
from services.account_service import (
    create_account
)

@router.message(
    AddAccountStates.waiting_owner_percent
)
async def percent_handler(
    message: Message,
    state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "Foizni son bilan kiriting."
        )
        return

    percent = int(message.text)

    data = await state.get_data()

    owners = data["owners"]

    current_index = data["current_index"]

    percents = data["percents"]

    percents.append(percent)

    current_index += 1

    if current_index < len(owners):

        await state.update_data(
            current_index=current_index,
            percents=percents
        )

        await message.answer(
            f"{owners[current_index]['name']} uchun foiz:"
        )

        return

    if sum(percents) != 100:

        await message.answer(
            "Foizlar yig'indisi 100 emas."
        )

        await state.clear()

        return

    for owner, percent in zip(
        owners,
        percents
    ):
        owner["percent"] = percent

    await create_account(
        account_number=data[
            "account_number"
        ],
        owners_data=owners
    )

    await message.answer(
        "✅ Akkount qo'shildi.",
        reply_markup = back_to_main_page()
    )


    await state.clear()


#Akkount o'chirish
@router.callback_query(
    F.data == "delete_account"
)
async def delete_account(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        DeleteAccountStates.waiting_account_number
    )

    await callback.message.answer(
        "Akkount raqamini kiriting:"
    )

#O'chirish
@router.message(
    DeleteAccountStates.waiting_account_number
)
async def delete_account_number(
    message: Message,
    state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "Faqat son kiriting."
        )
        return

    success = await delete_account(
        int(message.text)
    )

    if not success:

        await message.answer(
            "Bunday akkount topilmadi."
        )

        return

    await message.answer(
        "✅ Akkount o'chirildi.",
        reply_markup=back_to_main_page()
    )


    await state.clear()


