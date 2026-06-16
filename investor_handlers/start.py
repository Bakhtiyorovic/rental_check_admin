from aiogram import Router
from aiogram import F

from aiogram.filters import Command
from aiogram.types import Message
from services.investor_service import login_owner
from aiogram.fsm.context import FSMContext

from states.auth import AuthStates

router = Router()


@router.message(Command("start"))
async def start_handler(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        AuthStates.waiting_secret_code
    )

    await message.answer(
        "4 xonali kodingizni kiriting."
    )



@router.message(
    AuthStates.waiting_secret_code
)
async def code_handler(
    message: Message,
    state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "4 xonali kod kiriting."
        )
        return

    owner = await login_owner(
        int(message.text),
        message.from_user.id
    )

    if not owner:

        await message.answer(
            "Kod noto'g'ri."
        )
        return

    await state.clear()

    await message.answer(
        f"Assalomu alaykum "
        f"{owner.name}.\n\n"
        f"Sizning hisobotlaringiz shu yerga yuboriladi.\n\n"
        f'Shu yerdan hisoblaringizni olish mumkin /reports'
    )