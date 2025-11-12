import os
import re
import random
import time
from datetime import datetime
import telebot

# === TOKEN ===
TOKEN = os.getenv("TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Няма зададен TELEGRAM TOKEN в Render (Environment Variables).")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# махаме webhook, за да не блокира polling-а
try:
    bot.remove_webhook()
except Exception:
    pass

# === ПОСЛАНИЯ ===
ORACLE_MESSAGES = [
    "🌙 Понякога Вселената шепне най-силно, когато замълчиш.",
    "🕊️ Не търси светлината — бъди тя.",
    "🌸 Калинката каца само на хора, готови за промяна.",
    "💫 Това, което днес те боли, утре ще ти покаже пътя.",
    "🔥 Във всяка раздяла живее семето на ново начало.",
    "🌿 Всичко, което е истинско, винаги намира път към теб.",
    "🌹 Обичай смело, дори светът да те нарече наивна.",
    "✨ Не забравяй — чудесата идват при тези, които все още вярват."
]

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, greet_text(message.from_user.first_name))

@bot.message_handler(commands=['oracle'])
def oracle_cmd(message):
    bot.reply_to(message, random.choice(ORACLE_MESSAGES))

# === ШАБЛОНИ ===
THANKS_PAT = re.compile(r'\b(мерси|благодаря|благодар(?:я|а)|thanks|thank you)\b', re.IGNORECASE)
HOW_PAT    = re.compile(r'\b(как си|що правиш|какво правиш|как минава|how are you)\b', re.IGNORECASE)

last_greet = {}
GREET_COOLDOWN = 6 * 60 * 60  # 6 часа

def daytime_name():
    h = datetime.now().hour
    if 5 <= h < 12:  return "сутринта"
    if 12 <= h < 18: return "деня"
    if 18 <= h < 22: return "вечерта"
    return "нощта"

def greet_text(first_name: str) -> str:
    h = datetime.now().hour
    if 5 <= h < 12:
        g, extra = "☀️ Добро утро", "Нека денят ти започне с усмивка и светлина! 🌸"
    elif 12 <= h < 18:
        g, extra = "🌼 Добър ден", "Пожелавам ти вдъхновение и лека, успешна стъпка напред! 💫"
    elif 18 <= h < 22:
        g, extra = "🌇 Добър вечер", "Отпусни се и остави чудесата да дойдат при теб. 🌙"
    else:
        g, extra = "🌙 Спокойна нощ", "Сънища с добри духове и светлина. ✨"
    name = first_name or "приятелю"
    return f"{g}, {name}!\n{extra}\n\nАз съм Лиора 💫 — винаги до теб."

THANKS_REPLIES = [
    "С радост! 🌸 Ако искаш, кажи „изненадай ме“ и ще ти прошепна нещо красиво.",
    "Моля! ✨ Тук съм, когато ти потрябвам.",
    f"Светлина и от мен! 💫 Как върви {daytime_name()}?",
    "Благодарността ти топли сърцето ми. 🌷"
]

HOW_REPLIES = [
    "Добре съм — грея като малко слънце. ☀️ А ти как си?",
    "Тихо и светло ми е. ✨ Искаш ли послание — напиши „изненадай ме“.",
    f"Дишам в ритъма на доброто. 💫 Как минава {daytime_name()} при теб?",
    "Тук съм, слушам те. Разкажи ми нещо малко и истинско. 🌿"
]

# === РОУТЪР ===
@bot.message_handler(func=lambda m: bool(m.text))
def router(message):
    text = (message.text or "").strip()

    # 1. Игнорира команди
    if text.startswith('/'):
        return

    # 2. Благодарности
    if THANKS_PAT.search(text):
        bot.reply_to(message, random.choice(THANKS_REPLIES))
        return

    # 3. „Как си“
    if HOW_PAT.search(text):
        bot.reply_to(message, random.choice(HOW_REPLIES))
        return

    # 4. Поздрав (ако не е имало скоро)
    uid = message.from_user.id
    now = time.time()
    if now - last_greet.get(uid, 0) >= GREET_COOLDOWN:
        bot.reply_to(message, greet_text(message.from_user.first_name))
        last_greet[uid] = now
        return

    # 5. По желание — нищо повече, за да не се дублира

# === СТАРТ ===
if __name__ == "__main__":
    print("🌷 Лиора стартира...")
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=30)
