import logging
import os

from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

from dialogflow import detect_intent_texts


load_dotenv()
DF_PROJECT_ID=os.getenv('DF_PROJECT_ID')
TG_TOKEN=os.getenv('TG_TOKEN')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot: Bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def init_tg_logger(name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    tg_bot_logger = Bot(token=TG_TOKEN)
    logger.addHandler(TelegramLogsHandler(tg_bot_logger, os.getenv('TG_BOT_OWNER_CHAT_ID')))
    return logger


logger = init_tg_logger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def answer(update: Update, context: CallbackContext) -> None:
    try:
        answer = detect_intent_texts(DF_PROJECT_ID, update.message.from_user.id, [update.message.text,])
        update.message.reply_text(answer)
    except Exception as e:
        logger.exception('Произошла ошибка при получении ответа от DialofFlow')


def run_dialog_bot() -> None:
    updater = Updater("2081633148:AAHT53UQUP_e0raz82jOzovx6-3e8OM7Iik")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_dialog_bot()