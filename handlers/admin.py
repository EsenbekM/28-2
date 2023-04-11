from aiogram import types, Dispatcher
from config import dp, bot, ADMINS


async def ban(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.answer("Ты не мой хозяин!")
        elif not message.reply_to_message:
            await message.answer("Команда должна быть ответом на сообщение!")
        else:
            await message.delete()
            await bot.ban_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                until_date=60,
                revoke_messages=True
            )
            await message.answer(
                "Провосудие свершилось!\n"
                f"{message.reply_to_message.from_user.full_name} "
                f"забанен по воле {message.from_user.first_name}")
    else:
        await message.answer("Пиши в группу!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix="!/")
