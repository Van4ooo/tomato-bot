import asyncio
from time import strftime, time as now_time

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from _bot import bot
from keyboard.inline_buttons_to_timer import *

timer_router = Router(name=__name__)
timers = {}


def _init_chat(chat_id):
    if chat_id not in timers:
        timers[chat_id] = {'timers': [], 'id_timer': 0}


def filter_timer(chat_id):
    timers[chat_id]['timers'] = list(filter(lambda x: not x[0].done(), timers[chat_id]['timers']))


async def send_timer_expired_message(chat_id: int, message_id: int) -> None:
    await bot.send_message(chat_id=chat_id, text="Час вийшов!⏰⏰⏰", reply_to_message_id=message_id)


async def set_timer(time_seconds: int, chat_id: int, message_id: int) -> None:
    await asyncio.sleep(time_seconds)
    await send_timer_expired_message(chat_id, message_id)


async def add_new_timer(time: int, chat_id: int, message_id: int) -> None:
    timers[chat_id]['id_timer'] += 1
    filter_timer(chat_id=chat_id)

    if (c := timers[chat_id]['timers'].__len__()) == 3:  # 3 це максимальна к-сть одночасних таймерів для користувача
        await bot.send_message(chat_id=chat_id, text=f"Досягнутий ліміт на таймери {c}/{c}🙊",
                               reply_to_message_id=message_id)
        return

    timers[chat_id]['timers'].append((asyncio.create_task(
        set_timer(time * 60, chat_id, message_id)), time, timers[chat_id]['id_timer']))

    await bot.send_message(chat_id=chat_id, text=f"Таймер на {time} хвилин встановлено🥴",
                           reply_to_message_id=message_id,
                           reply_markup=buttons_to_timer(timers[chat_id]['id_timer'], now_time() + time * 60))


@timer_router.message(Command('5', '10', '15', '25'))
async def set_timer_command(message: Message):
    _init_chat(message.chat.id)
    time = int(message.text[1:].split()[0])

    await add_new_timer(time, message.chat.id, message.message_id)


@timer_router.message(Command('cancel'))
async def stop_timer_command(message: Message):
    _init_chat(message.chat.id)

    for timer in reversed(timers[message.chat.id]['timers']):
        if not timer[0].done():
            timer[0].cancel()
            await message.reply("Останній таймер було зупинено🫡")
            break
    else:
        await message.reply("У вас немає запущених таймерів👀")


@timer_router.message(Command('repeat'))
async def repeat_timer_command(message: Message):
    _init_chat(message.chat.id)
    if (rez := timers[message.chat.id]['timers']).__len__() > 0:
        await add_new_timer(rez[len(rez) - 1][1], message.chat.id, message.message_id)
    else:
        await message.reply("Ви ще не запускали таймерів")


def activ_timer(chat_id) -> int:
    return sum(not timer[0].done() for timer in timers[chat_id]['timers'])


@timer_router.message(Command('stats'))
async def stats_timer_command(message: Message):
    _init_chat(message.chat.id)

    await message.answer(f"Статистика користувача *{message.from_user.first_name}*"
                         f"\n\nАктивних таймерів - {activ_timer(message.chat.id)}/3"
                         f"\nСтворених таймерів {timers[message.chat.id]['id_timer']}",
                         parse_mode="Markdown")


@timer_router.message()
async def text_timer(message: Message):
    _init_chat(message.chat.id)

    try:
        _time = int(message.text.split()[0])
        if 0 > _time or _time > 180:
            await message.answer("Я можу ставити таймери в межах 1-180 хвилин👉👈")
            return
        await add_new_timer(_time, message.chat.id, message.message_id)
    except ValueError:
        await message.answer("Я не розумію 👉👈")


@timer_router.callback_query(F.data.startswith("cancel_timer"))
async def stop_timer_by_id(call: CallbackQuery):
    for timer in timers[call.message.chat.id]['timers']:
        if timer[2] == int(call.data.split()[1]) and not timer[0].done():
            timer[0].cancel()
            await call.answer("Таймер зупиненний🫡")
    else:
        await call.answer("Таймер вже не активний🤔")


@timer_router.callback_query(F.data.startswith("timer_time"))
async def timer_time(call: CallbackQuery):
    _, id_timer, _time = call.data.split()
    id_timer, _time = int(id_timer), float(_time)

    for timer in timers[call.message.chat.id]['timers']:
        if timer[2] == id_timer and not timer[0].done():
            time_dif = int(_time - now_time())
            h, remainder = divmod(time_dif, 3600)
            m, s = divmod(remainder, 60)

            await call.answer(f"Залишилося {h:02}:{m:02}:{s:02}")
    else:
        await call.answer("Таймер вже не активний🤔")


__all__ = ('timer_router',)
