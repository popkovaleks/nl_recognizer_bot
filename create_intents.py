import json
import argparse

from environs import Env


env = Env()
env.read_env()
PROJECT_ID=env('PROJECT_ID')
GOOGLE_APPLICATION_CREDENTIALS=env('GOOGLE_APPLICATION_CREDENTIALS')

def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', default='intent.json', help='Path to json file')

    args = parser.parse_args()
    path = args.p
    print(path)

    with open(path, 'r') as file:
        intentions_json = file.read()

    intentions = json.loads(intentions_json)
    print(intentions)

    for intention in intentions:
        print(intention)
        print('---')
        print(intentions[intention]['questions'])
        print(intentions[intention]['answer'])
        print('='*30)
        create_intent(PROJECT_ID, intention, intentions[intention]['questions'], [intentions[intention]['answer']])


if __name__ == '__main__':
    main()