import time
from twilio.rest import Client
import openai

#Import the Keys
from secret import TWILLIO_TOKEN
from secret import OPENAI_KEY
from secret import ACC_SID


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

# Receive a text message
def receive_message():
    # Get the last message sent to the Twilio number
    messages = client.messages.list(to=your_twilio_number)
    message = messages[0]
    return message.body, message.from_

# Send a text message
def send_message(message, sender):
    client.messages.create(
        to=sender,
        from_= your_twilio_number,
        body=message)

# Main function
def main():
    message, sender = receive_message()
    response = generate_response(message)
    send_message(response, sender)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(20)
