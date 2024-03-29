import os
import logging
import random

import vk_api as vk

from telegram import Bot
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from dialogflow import detect_intent_texts
from tg_bot import TelegramLogsHandler


logger = logging.getLogger(__file__)


def answer(event, vk_api, df_project_id, vk_session: vk.VkApi):
    fallback, answer = detect_intent_texts(df_project_id, vk_session.client_secret, event.text)
    if not fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1,1000)
        )


def main():
    load_dotenv()
    df_project_id = os.getenv('DF_PROJECT_ID')

    logging.basicConfig(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(Bot(token=os.getenv('TG_TOKEN')), os.getenv('TG_BOT_OWNER_CHAT_ID')))

    try:
        vk_session = vk.VkApi(token=os.getenv('VK_BOT_TOKEN'))
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
    except vk.VkApiError:
        logger.exception('Ошибка API ВК при установлении связи')
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    answer(event, vk_api, df_project_id, vk_session)
        except vk.VkApiError:
            logger.exception('Ошибка API ВК при обработке сообщений')


if __name__ == "__main__":
    main()
