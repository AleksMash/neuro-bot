import os
import random

import vk_api as vk

from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from dialogflow import detect_intent_texts

load_dotenv()
VK_BOT_TOKEN = os.getenv('VK_BOT_TOKEN')
DF_PROJECT_ID=os.getenv('DF_PROJECT_ID')


def echo(event, vk_api):
    answer = detect_intent_texts(DF_PROJECT_ID, vk_session.client_secret, [event.text,])
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=VK_BOT_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)