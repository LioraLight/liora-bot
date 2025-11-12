# app.py
# -*- coding: utf-8 -*-

import os
import random
from flask import Flask, request, abort
import telebot

# === ENV ===
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Липсва BOT_TOKEN (Render → Environment → BOT_TOKEN).")

# Render подава публичния URL в RENDER_EXTERNAL_URL
BASE_URL = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
if not BASE_URL:
    # Може да зададеш ръчно своя URL като WEBHOOK_URL_BASE, ако искаш
    BASE_URL = os.getenv("WEBHOOK_URL_BASE", "").rstrip("/")

if not BASE_URL:
    raise RuntimeError(
        "Липсва RENDER_EXTERNAL_URL/WEBHOOK_URL_BASE. "
        "След първия deploy копирай primary URL от Render и го запиши като WEBHOOK_URL_BASE."
    )

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)


# ========= Команди и отговори =========

@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    text = (
        "🌸 Здравей, аз съм <b>Лиора</b> — носителка на добро настроение!\n\n"
        "Кажи ми нещо като:\n"
        "❤️ <i>обичам те</i> — любовно послание\n"
        "😂 <i>шега</i> — за малко смях\n"
        "☀️ <i>как си</i> — да побъбрим\n"
        "🪄 <i>изненад(ай ме)</i> — за неочаквано послание\n\n"
        "Списък с команди: /start /hello /help"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "Напиши „шега“, „обичам те“, „как си“ или „изненадй ме“ ✨")


# 💌 Любов
@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ("обич", "обичам", "любов")))
def love_message(m):
    replies = [
        "💖 Истинската любов не вика — тя просто присъства.",
        "🌹 Обичта е най-тихата сила — и най-могъщата.",
        "✨ Някой някъде си помисли за теб — и светът стана по-топъл.",
        "💫 Любовта е начин да кажеш „тук съм“ без думи.",
    ]
    bot.reply_to(m, random.choice(replies))


# 😂 Шеги
@bot.message_handler(func=lambda m: m.text and "шега" in m.text.lower())
def jokes(m):
    jokes = [
        "😂 Защо компютърът е в депресия? — Защото има твърд диск и никакви емоции!",
        "🤣 Питат ме: „Как си?“ — „На батерия и надежда!“",
        "😄 Ако животът ти дава лимони — направи лимонада… и я продай с усмивка!",
        "😜 Не съм мързелива — в режим „енергоспестяване“ съм.",
    ]
    bot.reply_to(m, random.choice(jokes))


# 🌞 Разговорно
@bot.message_handler(func=lambda m: m.text and "как си" in m.text.lower())
def how_are_you(m):
    bot.reply_to(m, "Тихо и светло ми е ✨ А при теб как е денят?")


# 🎁 Изненада
@bot.message_handler(func=lambda m: m.text and "изненад" in m.text.lower())
def surprise(m):
    surprises = [
        "🎁 Не търси магията — тя си ти.",
        "🌼 Днес ще се случи нещо хубаво. Усмихни се!",
        "🕊️ Светът става по-красив, когато си спомниш кой си.",
        "💛 Бъди причина някой да повярва в доброто.",
    ]
    bot.reply_to(m, random.choice(surprises))


# Default
@bot.message_handler(func=lambda m: True)
def fallback(m):
    bot.reply_to(m, "🌟 Кажи „шега“, „обичам те“, „как си“ или „изненадй ме“ 💫")


# ========= Flask уебхук =========
