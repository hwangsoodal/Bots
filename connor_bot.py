from langchain_community.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage

import requests
import re
import telebot
import base64

# Initialize the bot with your token
bot = telebot.TeleBot('telebot')

client_id = "client_id"
client_secret = "client_secret"
credentials = f"{client_id}:{client_secret}"
base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

def load_prompt(url):
    match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
    if match_ is None:
        raise ValueError('Invalid Google Docs URL')
    doc_id = match_.group(1)

    response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
    response.raise_for_status()
    return response.text

def Answer(system, topic):
    chat = GigaChat(credentials=base64_credentials, scope='GIGACHAT_API_PERS', verify_ssl_certs=False)

    messages = [SystemMessage(content=system)]
    messages.append(HumanMessage(content=topic))
    res = chat(messages)
    messages.append(res)

    print("User: ", topic)
    print("Bot: ", res.content)

    return res.content

expert_prompt = load_prompt('google_doc')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я Коннор!")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    response = Answer(system=expert_prompt, topic=message.text)
    bot.reply_to(message, response)

bot.polling(none_stop=True)