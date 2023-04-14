from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import dp, bot
from .client_kb import start_markup
from aiogram.dispatcher.filters import Text



# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f"Салалекум {message.from_user.full_name}",
                           reply_markup=start_markup)
    # await message.answer("This is an answer method!", reply_markup=)
    # await message.reply("This is a reply method!", reply_markup=)


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


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(quiz_1, Text(equals='тест', ignore_case=True))
    dp.register_message_handler(help_command, commands=['help'])
