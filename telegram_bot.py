import logging

from environs import Env
from telegram import Update, Bot
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dialogflow_intent import detect_intent
from logger import TelegramLogHandler


def main():
    bot = Bot(token=TELEGRAM_TOKEN_LOGS)

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogHandler(bot, TG_CHAT_ID))

    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, response))

    updater.start_polling()
    updater.idle()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')
    detect_intent(
        project_id=PROJECT_ID,
        session_id=update.effective_chat.id,
        texts=update.message.text,
        language_code='ru-RU')


def response(update: Update, context: CallbackContext):
    session_id = update.effective_chat.id
    response_text = detect_intent(PROJECT_ID, session_id, update.message.text, 'ru')
    
    context.bot.send_message(chat_id=session_id, text=response.query_result.fulfillment_text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
    PROJECT_ID = env('PROJECT_ID')
    GOOGLE_APPLICATION_CREDENTIALS = env('GOOGLE_APPLICATION_CREDENTIALS')
    TELEGRAM_TOKEN_LOGS = env('TELEGRAM_TOKEN_LOGS')
    TG_CHAT_ID = env('TG_CHAT_ID')

    main()
