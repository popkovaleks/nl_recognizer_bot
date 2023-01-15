import random
import vk_api as vk

from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

from dialogflow_intent import detect_intent


env = Env()
env.read_env()

VK_TOKEN = env('VK_API_TOKEN')
PROJECT_ID=env('PROJECT_ID')
GOOGLE_APPLICATION_CREDENTIALS=env('GOOGLE_APPLICATION_CREDENTIALS')


def echo(event, vk_api):
    user_id = event.user_id
    message = event.text
    response_text = detect_intent(project_id=PROJECT_ID, session_id=user_id, texts=[message], language_code='ru')
    if response_text:
        vk_api.messages.send(
            user_id=user_id,
            message=response_text,
            random_id=random.randint(1,1000)
        )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)