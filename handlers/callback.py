from aiogram import types, Dispatcher
from config import dp, bot


# @dp.callback_query_handler(text="quiz_1_button")
async def quiz_2(call: types.CallbackQuery):
    question = "By whom invented Python?"
    answer = [
        "Harry Potter",
        "Putin",
        "Guido Van Rossum",
        "Voldemort",
        "Griffin",
        "Linus Torvalds",
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type="quiz",
        correct_option_id=3,
        explanation="Дурачок",
        open_period=10,
    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text="quiz_1_button")
