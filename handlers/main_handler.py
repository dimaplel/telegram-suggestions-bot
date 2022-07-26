import aiogram.utils.exceptions
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from datetime import datetime

from config import *
from create_bot import bot, cursor, base, is_banned


# Function to get user id from message more easy
def get_user_id(message: types.Message):
    if message.reply_to_message.text:
        user_id = message.reply_to_message.text.split()[-1].replace("*", "")
    else:
        user_id = message.reply_to_message.caption.split()[-1].replace("*", "")
    return user_id


# Function which answers to banned users based on availability of ban reason
async def answer_banned(user_id):
    cursor.execute(f'SELECT ban_reason FROM ban_id WHERE user_id = {user_id}')
    reason = cursor.fetchone()[0]
    if reason is None:
        await bot.send_message(chat_id=user_id, text=TEXT_MESSAGES['user_banned'])
    else:
        await bot.send_message(chat_id=user_id, text=TEXT_MESSAGES['user_reason_banned'].format(reason),
                               parse_mode='HTML')


# Starting message (when '/start' command is entered)
async def starting(message: types.Message):
    await message.answer(TEXT_MESSAGES['start'])


# Function which allows support team to reply on users' messages with any type of content
async def reply_to_user(message: types.Message):
    # Filtering basic replies from answers to bot and commands
    if not message.reply_to_message.from_user.is_bot or message.is_command():
        return

    user_id = get_user_id(message)
    # Checking if user was banned earlier
    if is_banned(user_id):
        await message.reply(TEXT_MESSAGES['is_banned'])
        return

    bot_message = await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                         message_id=message.message_id)  # Sending reply to user
    utc_time = datetime.utcnow()
    date_utc = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    # Inserting user_message_id and bot_message_id to implement message editing option on both sides
    # Time is needed to delete this row after some time passes
    cursor.execute(f"INSERT INTO message_id VALUES (%s, %s, %s)", (message.message_id,
                                                                   bot_message.message_id, date_utc))
    base.commit()


# Function, which forwards user's messages to chat
async def forward_handler(message: types.Message):
    user_id = message.from_user.id
    # Checking if user is banned
    if is_banned(user_id):
        await answer_banned(user_id)
        return

    # Defining type of the message
    if message.text and not message.is_command():
        await message.answer(TEXT_MESSAGES['pending'])
        text_user = TEXT_MESSAGES['message_template'].format(message.from_user.username, message.text + '\n\n',
                                                             user_id)
        bot_message = await bot.send_message(chat_id=CHAT_ID, parse_mode="HTML", text=text_user)
    # Stickers are not allowed from user's side because he might be not banned using reply
    elif message.sticker:
        await message.reply(TEXT_MESSAGES['unsupported_format'])
        return
    else:
        caption = TEXT_MESSAGES['message_template'].format(message.from_user.username,
                                                           message.caption + '\n\n' if message.caption is not None
                                                           else '', user_id)
        bot_message = await bot.copy_message(chat_id=CHAT_ID, from_chat_id=user_id, message_id=message.message_id,
                                             caption=caption, parse_mode='HTML')

    utc_time = datetime.utcnow()
    date_utc = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    # Inserting user_message_id and bot_message_id to implement message editing option on both sides
    # Time is needed to delete this row after some time passes
    cursor.execute(f"INSERT INTO message_id VALUES (%s, %s, %s)", (message.message_id,
                                                                   bot_message.message_id, date_utc))
    base.commit()


# Function which is responsible for editing responses in the chat and edit copied message from bot in private chat
async def chat_edited_messages(message: types.Message):
    if not message.reply_to_message.from_user.is_bot or message.is_command():
        return

    user_id = get_user_id(message)
    if is_banned(user_id):
        await message.reply(TEXT_MESSAGES['is_banned'])
        return

    cursor.execute(f"SELECT bot_message_id FROM message_id WHERE user_message_id = {message.message_id}")
    to_edit_id = cursor.fetchone()[0]
    # Defining type of the message
    if message.text:
        try:
            await bot.edit_message_text(chat_id=user_id, message_id=to_edit_id, text=message.text,
                                        parse_mode='Markdown')
        except Exception as e:
            if type(e) == aiogram.utils.exceptions.MessageToEditNotFound:
                await message.reply(TEXT_MESSAGES['message_not_found'])
    else:
        try:
            await bot.edit_message_caption(chat_id=user_id, message_id=to_edit_id, caption=message.caption,
                                           parse_mode="HTML")
        except Exception as e:
            if type(e) == aiogram.utils.exceptions.MessageNotModified:
                await message.reply(TEXT_MESSAGES['message_was_not_edited'])
            elif type(e) == aiogram.utils.exceptions.MessageToEditNotFound:
                await message.reply(TEXT_MESSAGES['message_not_found'])


# Function which is responsible for editing messages from users in private chat
async def private_edited_messages(message: types.Message):
    user_id = message.from_user.id
    # Checking if user was banned; if not, sending his message with his id in the end; else, telling him he was banned
    if is_banned(user_id):
        await answer_banned(user_id)
        return

    # Finding bot message to edit by looking for it in SQL table
    cursor.execute(f"SELECT bot_message_id FROM message_id WHERE user_message_id = {message.message_id}")
    to_edit_id = cursor.fetchone()[0]
    # Defining type of the message
    if message.text:
        text_user = TEXT_MESSAGES['message_template'].format(message.from_user.username, message.text + '\n\n',
                                                             user_id)
        # Trying to edit text. If not successful - message was not found in database
        try:
            await bot.edit_message_text(text=text_user, chat_id=CHAT_ID, message_id=to_edit_id,
                                        parse_mode="HTML")
        except Exception as e:
            if type(e) == aiogram.utils.exceptions.MessageToEditNotFound:
                await message.reply(TEXT_MESSAGES['message_not_found'])
    else:
        text_user = TEXT_MESSAGES['message_template'].format(message.from_user.username,
                                                             message.caption + '\n\n' if message.caption is not None
                                                             else '', user_id)
        # Bot can edit only caption and text, so if user or chat member is trying to edit photo/video itself, we notify
        # him that he cannot do it.
        try:
            await bot.edit_message_caption(chat_id=CHAT_ID, message_id=to_edit_id, caption=text_user,
                                           parse_mode="HTML")
        except Exception as e:
            if type(e) == aiogram.utils.exceptions.MessageNotModified:
                await message.reply(TEXT_MESSAGES['message_was_not_edited'])
            elif type(e) == aiogram.utils.exceptions.MessageToEditNotFound:
                await message.reply(TEXT_MESSAGES['message_not_found'])


# This function register all needed message handlers with filters and commands
def setup_dispatcher(dp: Dispatcher):
    dp.register_message_handler(starting, commands=["start"])    # Handler for '/start' command
    dp.register_message_handler(filters.IsReplyFilter(True), filters.IDFilter(chat_id=CHAT_ID), reply_to_user,
                                is_reply=True, content_types=['any'])    # Handler for replying to user
    # Handler for forwarding users' messages to chat
    dp.register_message_handler(forward_handler, chat_type='private', content_types=['any'])
    # Handler for editing chat messages
    dp.register_edited_message_handler(filters.IsReplyFilter(True), filters.IDFilter(chat_id=CHAT_ID),
                                       chat_edited_messages, is_reply=True, content_types=['any'])
    # Handler for editing users' messages
    dp.register_edited_message_handler(private_edited_messages, content_types=['any'], chat_type='private')
