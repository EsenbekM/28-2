from aiogram import types, Dispatcher
from config import dp, bot


# @dp.message_handler()
# DRY - Don't Repeat Yourself
async def filter_bad_words(message: types.Message):
    bad_words = ["html", "java", "js", "дурак", "жинди"]
    user = f"@{message.from_user.username}" \
        if message.from_user.username else message.from_user.full_name
    for word in bad_words:
        if word in message.text.lower().replace(" ", ""):
            await message.answer(
                f"Не матерись {user}!\n"
                f"Сам ты {word}!"
            )
            # await bot.delete_message(message.chat.id, message.message_id)
            await message.delete()

    if message.text.startswith("."):
        # await bot.pin_chat_message(message.chat.id, message.message_id)
        await message.pin()

    if message.text == "dice":
        # await bot.send_dice()
        a = await message.answer_dice(emoji="🎲")
        # print(a.dice.value)


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(filter_bad_words)
