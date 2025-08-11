import time
import logging
from twilio.rest import Client
import openai

#Import the Keys
from secret import TWILLIO_TOKEN
from secret import OPENAI_KEY
from secret import ACC_SID


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Twilio account information
account_sid = ACC_SID
auth_token = TWILLIO_TOKEN
client = Client(account_sid, auth_token)

# OpenAI API key
openai.api_key = OPENAI_KEY

#TWILLIO NUMBER
your_twilio_number = '+18446172010'

# Function to generate response from OpenAI
def generate_response(prompt):
    try:
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = completions.choices[0].text
        return message.strip()
    except Exception as e:
        logger.exception("Error generating response from OpenAI API: %s", e)
        return "I'm sorry, I couldn't process your request."

# Receive a text message
def receive_message():
    try:
        # Get the last message sent to the Twilio number
        messages = client.messages.list(to=your_twilio_number)
        message = messages[0]
        return message.body, message.from_
    except Exception as e:
        logger.exception("Error receiving message from Twilio: %s", e)
        return None, None

# Send a text message
def send_message(message, sender):
    try:
        client.messages.create(
            to=sender,
            from_= your_twilio_number,
            body=message)
    except Exception as e:
        logger.exception("Error sending message via Twilio: %s", e)

# Main function
def main():
    message, sender = receive_message()
    if not message or not sender:
        logger.warning("No message received or sender missing.")
        return
    response = generate_response(message)
    if response:
        send_message(response, sender)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(20)
