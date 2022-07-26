from create_bot import base, cursor, is_banned, bot
from handlers import main_handler
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from config import *


# Function which helps to prevent SQL error (if chat participant answers to bot informing message)
def check_replied(message: types.Message):
    if message.text:
        if message.text.split()[-2].replace("*", "") != "id:":
            return False
    else:
        if message.caption.split()[-2].replace("*", "") != "id:":
            return False
    return True


# Function to ban user from writing to this bot using SQL
async def ban_user(message: types.Message):
    if not check_replied(message.reply_to_message):
        await message.reply(TEXT_MESSAGES['reply_error'])
        return

    user_id = main_handler.get_user_id(message)     # Getting user's id from the end of the message sent by bot
    try:
        reason = message.text.split(' ', maxsplit=1)[1]
    except Exception:
        reason = None
    if is_banned(user_id):
        await message.answer(TEXT_MESSAGES['already_banned'])  # If this user is already banned, we inform about it
    else:
        cursor.execute(f"INSERT INTO ban_id VALUES (%s, %s)", (user_id, reason))  # Inserting user into table
        base.commit()
        await message.reply(TEXT_MESSAGES['has_banned'])  # Informing that this user has been banned
        await main_handler.answer_banned(user_id)


# Function to unban user from ban list
async def unban_user(message: types.Message):
    if not check_replied(message.reply_to_message):
        await message.reply(TEXT_MESSAGES['reply_error'])
        return

    user_id = main_handler.get_user_id(message)     # Getting user's id from the end of the message sent by bot
    if is_banned(user_id):
        cursor.execute(f"DELETE FROM ban_id WHERE user_id = {user_id}")  # Deleting user from ban list if it was found
        base.commit()
        await message.reply(TEXT_MESSAGES['has_unbanned'])  # Informing that this user is unbanned now
        await bot.send_message(chat_id=user_id, text=TEXT_MESSAGES['user_unbanned'])
    else:
        await message.reply(TEXT_MESSAGES['not_banned'])  # If user is not banned, we inform aboit it


# Registering all dispatchers with their filters and commands
def setup_dispatcher(dp: Dispatcher):
    dp.register_message_handler(filters.IsReplyFilter(True), filters.IDFilter(chat_id=CHAT_ID), ban_user,
                                commands=["ban"], is_reply=True)  # Handler for '/ban' command
    dp.register_message_handler(filters.IsReplyFilter(True), filters.IDFilter(chat_id=CHAT_ID), unban_user,
                                commands=["unban"], is_reply=True)  # Handler for '/unban' command
