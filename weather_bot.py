# -*- coding: utf-8 -*-
"""weather_bot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z0JyQpQoFACZ5a0peLDbP2aKz3B_N9FS
"""

# WEATHER BOT
!pip install pyTelegramBotAPI requests

import telebot
import requests
import json

TELEGRAM_API_KEY = '7118016152:AAHDSr-6RLKHbNYM88SSpiYO_Cz6M73aHSA'
OPENWEATHER_API_KEY = '946dae0a9e631400680eed94f0ac04d5'
bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello!Welcome Weather_Bot👋 Send me a city name and I'll provide the current temperature.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message)
    city_name = message.text
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}')
    data = json.loads(response.text)
    if data['cod'] == 200:
        temp = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        bot.reply_to(message, f'The current temperature in {city_name} is {temp:.2f}°C.')
    else:
        bot.reply_to(message, 'Sorry, I could not find that city.')

bot.polling()

"""# New Section"""