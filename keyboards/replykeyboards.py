from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Akkountlar"),],
        [KeyboardButton(text="Hisobotlar")],
        [KeyboardButton(text="Oylik hisobotlar"), KeyboardButton(text="Akkount statuslar")]
    ],
    resize_keyboard=True
)
