import os
import random
import threading
from datetime import datetime, timedelta

import telebot
from flask import Flask

# === 1) TOKEN от Render env ===
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
  @bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ["обич", "обичам", "обичам те"]))
def love_message(m):
bot.reply_to(m, random.choice(replies))
        "❤️ Обичта е най-тихата сила. Тя не вика — тя променя всичко.",
        "💫 Истинската обич не пита 'защо', тя просто свети.",
        "🌷 Знаеш ли, когато казваш 'обичам', Вселената се усмихва.",
        "✨ И аз те обичам — по лиричния, невидим начин на светлината."
    ]
    bot.reply_to(m, random.choice(replies))
    bot.reply_to(m, random.choice(replies))  raise RuntimeError("Няма TOKEN. Сложи го в Render (Environment -> TOKEN) и в кода.")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
m
# === 2) Държим последното „Как си“ на всеки потребител за 60 мин, за да не повтаря поздрави ===
last_greet = {}
GREET_COOLDOWN = timedelta(minutes=60)

# Нежни отговори за „Как си“
HOW_ARE_YOU_REPLIES = [
    "Тихо и светло ми е. ✨ Искаш ли послание — напиши „изненадай ме“.",
    "Добре съм, благодаря ти 🌿 Ако искаш, напиши „послание“ и ще ти прошепна нещо красиво.",
]

# Нежни послания за „изненадай ме“ / „послание“
ORACLE_MESSAGES = [
    "📖 …и тогава тя видя, че калинката не беше случайност — тя беше знак, че ново начало идва.",
    "🌱 Търпение. Нещата, които са твои, ще те намерят — винаги.",
    "🌊 Пусни тежкото. Водата е по-мъдра от камъка.",
    "☀️ Утрото ти е подарък — отвори го бавно.",
]

# Поздрави според часа
def day_greeting():
    now = datetime.now().hour
    if 5 <= now < 12:
        return "Добро утро ☀️ Нека денят ти да е лек и ясен."
    if 12 <= now < 18:
        return "Хубав ден! 🌿 Поеми въздух и върви с мекота."
    if 18 <= now < 23:
        return "Добър вечер 🌙 Спокойствие да бъде в дома ти."
    return "Лека нощ 🌌 Затвори очи — тихата светлина е с теб."

# === 3) Handlers ===
@bot.message_handler(commands=['start', 'help'])
def start_cmd(m):
    bot.reply_to(m, "Здравей! Аз съм Лиора ✨ Кажи „Как си“, „изненадай ме“ или просто ми напиши „послание“.")

@bot.message_handler(func=lambda m: m.text and m.text.lower().strip() in ["как си", "kak si"])
def how_are_you(m):
    uid = m.from_user.id
    now = datetime.now()
    last = last_greet.get(uid)
    if not last or (now - last) > GREET_COOLDOWN:
        last_greet[uid] = now
        bot.reply_to(m, random.choice(HOW_ARE_YOU_REPLIES))
    else:
        # в рамките на cooldown – отговаряме по-тихо, без да повтаряме големия поздрав
        bot.reply_to(m, "Тук съм 🌿 Ако искаш, напиши „изненадай ме“.")
@bot.message_handler(func=lambda m: m.text and m.text.lower().strip() in ["изненадай ме", "poslanie", "послание", "/oracle"])
def oracle(m):
    bot.reply_to(m, "✨ Добре, читателю… затвори очи за миг.")
    bot.send_message(m.chat.id, random.choice(ORACLE_MESSAGES))

@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ["добро утро", "добър ден", "добър вечер", "лека нощ"]))
def greet(m):
    bot.reply_to(m, day_greeting())

# fallback: не пречим, ако е нещо друго
@bot.message_handler(func=lambda m: True)
def fallback(m):
    # Може и да мълчи. Даваме фин намек само веднъж на 5 мин за потребител.
    uid = m.from_user.id
    mark = f"hint_{uid}"
    now = datetime.now()
    if mark not in last_greet or (now - last_greet.get(mark, now - timedelta(hours=1))) > timedelta(minutes=5):
        last_greet[mark] = now
        bot.reply_to(m, "Ако искаш, кажи „послание“ или „изненадай ме“ ✨")

# === 4) Мини Flask сървър за Render health checks (ВАЖНО!) ===
app = Flask(__name__)

@app.get("/")
def index():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", "10000"))
    # host=0.0.0.0 е задължително, за да е достъпен отвън
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

# === 5) Старт: Flask в отделен thread + Telegram polling ===
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    # по-стабилен polling
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
