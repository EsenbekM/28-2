from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.dispatcher.filters import Text

from config import bot
from .client_kb import start_markup
from database.bot_db import sql_command_random, sql_command_all_users, sql_command_insert_user
from .utils import get_ids_from_users
from parser.series import parser


async def start_command(message: types.Message):
    users = await sql_command_all_users()
    ids = get_ids_from_users(users)
    if message.from_user.id not in ids:
        await sql_command_insert_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name
        )
    await bot.send_message(message.from_user.id, f"Салалекум {message.from_user.full_name}",
                           reply_markup=start_markup)


async def help_command(message: types.Message):
    await message.reply("Сам разбирайся!")


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="quiz_1_button")
    markup.add(button_1)

    question = "Когда была революция?"
    answer = [
        "07.04.2010",
        "21.04.2005",
        "07.04.2005",
        "07.05.2005",
        "13.04.2015",
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type="quiz",
        correct_option_id=0,
        explanation="Дурачок",
        open_period=10,
        reply_markup=markup
    )
    # await message.answer_poll()


async def get_random_anketa(message: types.Message):
    random_user = await sql_command_random()
    info = f"{random_user[3]} {random_user[4]} " \
           f"{random_user[5]} {random_user[6]}"
    info += f"\n\n@{random_user[2]}" if random_user[2] else ""

    await message.answer_photo(random_user[-1], caption=info)


async def get_series(message: types.Message):
    size = message.text.split()[-1] \
        if len(message.text.split()) == 2 else None
    series: list[dict] = parser(size)
    for serial in series:
        # await message.answer_photo(
        #     photo=serial['image'],
        #     caption=f"{serial['url']}\n\n"
        #             f"{serial['title']}\n"
        #             f"{serial['status']}\n"
        #             f"#Y{serial['year']} "
        #             f"#{serial['genre']} "
        #             f"#{serial['country']}"
        # )
        await message.answer(
            f"<a href='{serial['url']}'><b>{serial['title']}</b></a>\n"
            f"{serial['status']}\n"
            f"#Y{serial['year']} "
            f"#{serial['genre']} "
            f"#{serial['country']}",
            parse_mode=ParseMode.HTML
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(quiz_1, Text(equals='тест', ignore_case=True))
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(get_random_anketa, commands=['get'])
    dp.register_message_handler(get_series, commands=['series'])
