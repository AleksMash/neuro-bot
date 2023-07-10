from google.cloud import dialogflow
import os
import argparse
import json
import sys

from dotenv import load_dotenv


load_dotenv()
DF_PROJECT_ID=os.getenv('DF_PROJECT_ID')


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--file", help="Path to the file, containing train phrases.  Required.", required=True
    )

    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as training_file:
        training_phrases: str = training_file.read()

    training_phrases: dict = json.loads(training_phrases, )

    display_name = 'Устройство на работу'
    training_phrases_parts = training_phrases[display_name]['questions']
    message_texts = [training_phrases[display_name]['answer'],]

    create_intent(DF_PROJECT_ID, display_name, training_phrases_parts, message_texts)