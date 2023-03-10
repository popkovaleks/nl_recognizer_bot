import random
import vk_api as vk
import logging

from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from telegram import Bot

from dialogflow_intent import detect_intent
from logger import TelegramLogHandler


logger = logging.getLogger('Logger')


def send_response(event, vk_api, PROJECT_ID):
    user_id = event.user_id
    message = event.text
    response = detect_intent(project_id=PROJECT_ID,
                                  session_id=user_id,
                                  text=message,
                                  language_code='ru')
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()

    VK_TOKEN = env('VK_API_TOKEN')
    PROJECT_ID = env('PROJECT_ID')
    TELEGRAM_TOKEN_LOGS = env('TELEGRAM_TOKEN_LOGS')
    TG_CHAT_ID = env('TG_CHAT_ID')

    bot = Bot(token=TELEGRAM_TOKEN_LOGS)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogHandler(bot, TG_CHAT_ID))

    vk_session = vk.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_response(event, vk_api, PROJECT_ID)


if __name__ == "__main__":
    main()
