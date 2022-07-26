import aiogram.utils.executor
import logging
from create_bot import dp
from handlers import main_handler, admin_handler

# Setting logging to info level
logging.basicConfig(level=logging.INFO)  # Setting terminal logging to info mode

# Registering message handlers
admin_handler.setup_dispatcher(dp)
main_handler.setup_dispatcher(dp)

if __name__ == "__main__":
    aiogram.utils.executor.start_polling(dp)  # Starting to poll our bot
