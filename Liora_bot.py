import os
import time
import threading

import telebot
from telebot import apihelper
from flask import Flask

# Вариант A: ползвай TOKEN от Render (Environment)
TOKEN = os.getenv("TOKEN")
# Вариант B (ако нямаш Environment променлива): въведи тук токена си и махни коментара на следния ред:
# TOKEN = "PASTE_YOUR_TOKEN"

if not TOKEN:
    raise RuntimeError("Няма TOKEN. Сложи го в Render (Environment -> TOKEN) или в кода.")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ---- Хендлъри ----
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🌷 Здравей! Аз съм Лиора. Напиши „изненадай ме“ или /oracle.")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    text = (message.text or "").lower().strip()
    if text in ["изненадай ме", "oracle", "/oracle"]:
        bot.send_message(
            message.chat.id,
            "✨ Добре, читателю… затвори очи за миг.\n\n"
            "📖 …и тогава тя видя, че калинката не беше случайност — тя беше знак, че ново начало идва.\n\n"
            "🌸 Две нишки — една светлина. Послание и спомен, свързани за теб."
        )
    else:
        bot.send_message(
            message.chat.id,
            "🌼 Лиора те чу. Напиши „изненадай ме“ и ще ти прошепна нещо красиво."
        )

# ---- Безопасен polling (анти-409) ----
def safe_polling():
    while True:
        try:
            # ако е останал стар webhook – махни го
            try:
                bot.remove_webhook()
            except Exception:
                pass

            # стабилен polling
            bot.infinity_polling(timeout=20, long_polling_timeout=30, skip_pending=True)

        except apihelper.ApiTelegramException as e:
            status = getattr(getattr(e, "result", None), "status_code", None)
            if status == 409:
                print("⚠️ 409 Conflict: друга инстанция/стар webhook. Опит пак след 20 сек.")
                time.sleep(20)
                continue
            print(f"🚨 Telegram API error: {e}. Рестарт след 10 сек.")
            time.sleep(10)

        except Exception as e:
            print(f"❗ Неочаквана грешка: {e}. Рестарт след 5 сек.")
            time.sleep(5)

# ---- Flask keep-alive за Render (порт binding) ----
app = Flask(__name__)

@app.get("/")
def home():
    return "Liora is alive."

def run_flask():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ---- Старт ----
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("🌷 Лиора стартира…")
    safe_polling()
