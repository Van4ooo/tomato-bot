from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboard.menu import menu
from routers.uk_conf import *

main_command_router = Router(name=__name__)


@main_command_router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Здоров був *{message.from_user.first_name}🫡*\n"
                         f"{start_help_text}", parse_mode='Markdown',
                         reply_markup=menu())


@main_command_router.message(Command('help', '--help'))
async def _help(message: Message):
    await message.answer(start_help_text, parse_mode='Markdown')


@main_command_router.message(Command('t'))
async def _t(message: Message):
    await message.answer("Доступні лише такі команди - /5 /10 /15 /25")


__all__ = ('main_command_router',)
