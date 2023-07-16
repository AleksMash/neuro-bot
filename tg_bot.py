import logging
import os

from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

from dialogflow import detect_intent_texts


DF_PROJECT_ID: str
TG_TOKEN: str

logger = logging.getLogger(__file__)

class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot: Bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def error_handler(update: Update, context: CallbackContext):
    """loggint PTB errors"""
    logger.error(context.error)


def answer(update: Update, context: CallbackContext) -> None:
    fallback, answer = detect_intent_texts(DF_PROJECT_ID, update.message.from_user.id, [update.message.text, ])
    update.message.reply_text(answer)


def run_dialog_bot() -> None:
    global DF_PROJECT_ID, TG_TOKEN
    load_dotenv()
    DF_PROJECT_ID = os.getenv('DF_PROJECT_ID')
    TG_TOKEN = os.getenv('TG_TOKEN')

    logging.basicConfig(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(Bot(token=TG_TOKEN), os.getenv('TG_BOT_OWNER_CHAT_ID')))

    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_dialog_bot()