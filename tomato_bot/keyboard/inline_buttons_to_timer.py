from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def buttons_to_timer(id_timer: int, comp_time: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🕓", callback_data=f"timer_time {id_timer} {comp_time}"),
        InlineKeyboardButton(text="stop", callback_data=f"cancel_timer {id_timer}"),
    ]])
