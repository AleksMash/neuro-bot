import logging
import os

from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

from dialogflow import detect_intent_texts
from log_handlers import TelegramLogsHandler


logger = logging.getLogger(__file__)


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
    fallback, answer = detect_intent_texts(os.getenv('DF_PROJECT_ID'), update.message.from_user.id, update.message.text)
    update.message.reply_text(answer)


def run_dialog_bot() -> None:
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')

    logging.basicConfig(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(Bot(token=tg_token), os.getenv('TG_BOT_OWNER_CHAT_ID')))

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_dialog_bot()
