import telebot
import random
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# 🌷 Представяне
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(
        message,
        "🌸 Здравей, аз съм Лиора! Обичам да нося добро настроение ✨\n"
        "Кажи ми нещо като:\n"
        "❤️ „обичам те“ — за послание на любов\n"
        "😂 „шега“ — за малко смях\n"
        "☀️ „как си“ — за разговор\n"
        "🪄 или „изненадй ме“ — за неочаквано послание"
    )

# 💌 Любовни послания
@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ["обич", "обичам", "любов"]))
def love_message(m):
    replies = [
        "💖 Истинската любов не вика — тя просто присъства.",
        "🌹 Обичта е най-тихата сила — и най-могъщата.",
        "✨ Някой някъде си помисли за теб — и светът стана по-топъл.",
        "💫 Любовта е начин да кажеш „тук съм“ без думи."
    ]
    bot.reply_to(m, random.choice(replies))

# 😂 Шеги
@bot.message_handler(func=lambda m: "шега" in m.text.lower())
def jokes(m):
    jokes = [
        "😂 Защо компютърът е в депресия? — Защото има твърд диск и никакви емоции!",
        "🤣 Питат ме: ‘Как си?’ — Отговарям: ‘На батерия и надежда!’",
        "😄 Ако животът ти дава лимони — направи лимонада и я продай с усмивка!",
        "😜 Не съм мързелива, просто съм в режим на енергоспестяване."
    ]
    bot.reply_to(m, random.choice(jokes))

# 🌞 Разговорно
@bot.message_handler(func=lambda m: "как си" in m.text.lower())
def how_are_you(m):
    bot.reply_to(m, "Тихо и светло ми е ✨ А на теб как ти е денят?")

# 🎁 Изненада
@bot.message_handler(func=lambda m: "изненад" in m.text.lower())
def surprise(m):
    surprises = [
        "🎁 Не търси магията — тя си ти.",
        "🌼 Днес ще се случи нещо хубаво. Усмихни се!",
        "🕊️ Светът става по-красив, когато си спомниш кой си.",
        "💛 Бъди причина някой да повярва в доброто."
    ]
    bot.reply_to(m, random.choice(surprises))

# 💤 Безусловен отговор
@bot.message_handler(func=lambda m: True)
def default_reply(m):
    bot.reply_to(m, "🌟 Кажи „шега“, „обичам те“ или „изненадй ме“ 💫")

# 🕊️ Старт
bot.polling(none_stop=True)
