import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dialogflow_intent import detect_intent


env = Env()
env.read_env()
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
PROJECT_ID=env('PROJECT_ID')
GOOGLE_APPLICATION_CREDENTIALS=env('GOOGLE_APPLICATION_CREDENTIALS')


def main():
    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )   
    logger = logging.getLogger(__name__)

    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()



def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')
    detect_intent(project_id=PROJECT_ID, session_id=update.effective_chat.id, texts=update.message.text, language_code='ru-RU')
    print(update)
    print('------')
    print(update.effective_chat)

def echo(update: Update, context: CallbackContext):
    # context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    session_id = update.effective_chat.id
    response_text = detect_intent(PROJECT_ID, session_id, [update.message.text], 'ru')
    context.bot.send_message(chat_id=session_id, text=response_text)

if __name__ == '__main__':
    main()