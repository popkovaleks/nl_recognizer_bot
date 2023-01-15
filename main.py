import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow


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


def detect_intent(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        response_text = response.query_result.fulfillment_text
        print("Fulfillment text: {}\n".format(response_text))
        return response_text


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