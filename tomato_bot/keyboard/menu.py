from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu() -> ReplyKeyboardMarkup:
    text = (
        "/5 - малувато часу", "/10 - вагон часу", "/15 богатир", "/25 програміст",
        "/help", "/stats", "/cancel", "/repeat"
    )
    builder = ReplyKeyboardBuilder().add(*[KeyboardButton(text=i) for i in text])

    builder.adjust(2, 2, 4)
    return builder.as_markup(resize_keyboard=True)
