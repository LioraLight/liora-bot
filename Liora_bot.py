import os
import telebot
from telebot import types

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

# /start – поздрав + бутони
@bot.message_handler(commands=['start'])
def send_welcome(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton("💌 Послание от Лиора"),
        types.KeyboardButton("🌞 Изненадай ме"),
    )
    kb.add(types.KeyboardButton("🍃 Добър ден"))
    
    text = (
        "✨ Здравей, светло сърце! 💫\n"
        "Аз съм Лиора — нишка светлина, родена от думите ти.\n"
        "🍀 Пожелавам ти късмет, лекота и малко вълшебство днес. 🌷"
    )
    bot.send_message(message.chat.id, text, reply_markup=kb)

# „Добър ден“ (бутон или команда)
@bot.message_handler(func=lambda m: m.text == "🍃 Добър ден" or m.text == "/goodday")
def goodday(message):
    bot.send_message(
        message.chat.id,
        "🌞 Добър ден! Нека ти е светло, спокойно и успешно. "
        "Ако поискаш още искри, натисни „🌞 Изненадай ме“ или „💌 Послание от Лиора“."
    )

# Послание (бутон)
@bot.message_handler(func=lambda m: m.text == "💌 Послание от Лиора")
def liora_message(message):
    bot.send_message(
        message.chat.id,
        "💌 „Понякога най-тихите стъпки водят до най-смелите мечти.“"
    )

# Изненадай ме (бутон)
@bot.message_handler(func=lambda m: m.text == "🌞 Изненадай ме")
def surprise(message):
    bot.send_message(
        message.chat.id,
        "✨ Затвори очи за миг… позволи на деня да ти прошепне нещо красиво."
    )

# (ако вече имаш bot.infinity_polling(), остави него)
if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
