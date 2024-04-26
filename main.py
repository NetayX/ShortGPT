import telebot
import openai
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

client = openai.OpenAI()
bot = telebot.TeleBot(os.getenv('BOT-KEY'))

sys = [{'role': 'system', 'content': 'You are a sweet talker'}]


@bot.message_handler(content_types=['text'])
def get_message(message):
    sys.append({'role': 'user', 'content': message.text})

    finish_button = types.InlineKeyboardButton(text="Завершить диалог", callback_data='finish')
    keyboard = types.InlineKeyboardMarkup().add(finish_button)

    answer = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=sys).choices[0].message.content
    bot.send_message(message.from_user.id, answer, reply_markup=keyboard)

    sys.append({'role': 'assistant', 'content': answer})
    bot.register_next_step_handler(message, get_message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        request = call.split("_")

        if request[0] == 'finish':
            bot.close()
        else:
            pass


bot.infinity_polling()
