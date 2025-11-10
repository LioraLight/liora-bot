from flask import Flask
import telebot
import os

TOKEN = os.environ.get("TOKEN", "тук_впиши_твоят_токен")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "🌸 LioraLightBot is alive!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🌷 Здравей, аз съм Лиора. Готова съм да внеса светлина в деня ти.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    if "изненад" in text:
        bot.send_message(message.chat.id, "🌸 Добре, читателю... затвори очи за миг и почувствай.")
    else:
        bot.send_message(message.chat.id, "🌼 Лиора те чу. Напиши „изненадaй ме“.")

if __name__ == "__main__":
    bot.polling(non_stop=True)
    app.run(host="0.0.0.0", port=10000)
