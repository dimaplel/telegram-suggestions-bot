import psycopg2.extras

from aiogram import Bot, Dispatcher
from config import *

# Creating bot and dispatcher with built-in functions
bot = Bot(TOKEN)
dp = Dispatcher(bot)

# Creating and accessing database for banning/unbanning users and editing messages
base = psycopg2.connect(host=HOSTNAME, dbname=DATABASE, user=USERNAME, password=DB_PASS, port=PORT_ID)
cursor = base.cursor(cursor_factory=psycopg2.extras.DictCursor)
try:
    cursor.execute(f'CREATE TABLE IF NOT EXISTS ban_id (user_id int PRIMARY KEY, ban_reason text)')
    cursor.execute(f'CREATE TABLE IF NOT EXISTS message_id (user_message_id int, bot_message_id int, datatime '
                   f'timestamp)')
    base.commit()
    print("[LOG] Database accessed!")
except Exception as e:
    print(e)


# Function for checking if user is banned
def is_banned(user_id):
    cursor.execute(f"SELECT user_id FROM ban_id WHERE user_id = {user_id}")
    return True if cursor.fetchone() else False
