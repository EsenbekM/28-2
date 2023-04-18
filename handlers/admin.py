from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import dp, bot, ADMINS
from database.bot_db import sql_command_all, sql_command_delete


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


async def delete_data(message: types.Message):
    users = await sql_command_all()
    for user in users:
        info = f"{user[3]} {user[4]} " \
               f"{user[5]} {user[6]}"
        info += f"\n\n@{user[2]}" if user[2] else ""
        await message.answer_photo(
            user[-1], caption=info,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f"DELETE {user[3]}",
                    callback_data=f"delete {user[0]}"
                )
            )
        )


async def complete_delete(call: types.CallbackQuery):
    user_id = call.data.replace("delete ", "")
    await sql_command_delete(user_id)
    await call.answer(text=f"Удален пользователь с id {user_id}",
                      show_alert=True)
    await call.message.delete()
    # await bot.delete_message(call.from_user.id, call.message.message_id)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix="!/")
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(
        complete_delete,
        lambda call: call.data and call.data.startswith("delete ")
    )
