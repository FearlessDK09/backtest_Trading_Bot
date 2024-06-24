import telegram
from config.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_IDS

def post_message(message):
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        for chat_id in TELEGRAM_CHAT_IDS:
            bot.send_message(chat_id, message)
    except Exception as e:
        print("Error sending message:", e)
