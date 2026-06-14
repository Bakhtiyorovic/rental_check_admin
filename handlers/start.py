from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from keyboards.replykeyboards import rkb

router = Router()  # Bu modul uchun Router

# /start komandasi
@router.message(Command("start"))
async def cmd_start(message: Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"Salom, {user_name}! 👋\n"
        "Men admin xizmat ko'rsatuvchi Telegram botman.\n",
        reply_markup=rkb
    )


@router.callback_query(F.data == "cmd_start")
async def back_to_start_callback(callback: CallbackQuery):
    user_name = callback.from_user.first_name

    # Eskidan qolgan inline tugmalarni o'chirib tashlash uchun eski xabarni o'chiramiz
    await callback.message.delete()

    # Yangidan xabar yuboramiz va rkb (Reply Keyboard) ni chiqaramiz
    await callback.message.answer(
        f" {user_name}! 👋\n"
        "Siz asosiy sahifaga qaytdingiz.\n",
        reply_markup=rkb
    )

    # Telegram tepasida aylanib turadigan yuklanish belgisini yo'qotish uchun:
    await callback.answer()