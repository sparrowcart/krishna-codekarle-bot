import asyncio
import datetime
import json
import random
import threading
from flask import Flask
from telegram import Bot
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 🔐 Personal config
BOT_TOKEN = '7821824837:AAEtpcx7wCCg1hbUAGz0Tl98HlntHx5athE'
USER_ID = 1755221416  # Krishna Only

# 🧠 Load tips from JSON
with open('tips.json', 'r', encoding='utf-8') as f:
    tips = json.load(f)

# 🎯 Motivational Daant
motivations = [
    "Code kar le Krishna! Coffee nahi chahiye, logic chahiye!",
    "Framework sirf tab kaam aayega jab base strong hoga. JS padho!",
    "Bug se darr nahi lagta sahab, deploy karne se lagta hai!",
    "BraveMoor CEO banna hai? Pehle daily code push kar!",
    "Distraction hata, IDE khol, aur Krishna mode ON kar!",
    "Galti se mat dar, error se seekh!",
]

# 📩 Send Motivational Reminder
async def send_reminder():
    bot = Bot(token=BOT_TOKEN)
    now = datetime.datetime.now()
    hour = now.hour
    if hour == 9:
        msg = "🌞 Subah ho gayi Krishna bhai! Bina code likhe scroll mat maar!"
    elif hour == 14:
        msg = "🧠 Dopahar ka time hai, dimag fresh hai — JavaScript ke bugs tod!"
    elif hour == 19:
        msg = "🌇 Shaam ka waqt hai, Netflix nahi, codeflix dekh bhai!"
    else:
        msg = random.choice(motivations)

    await bot.send_message(chat_id=USER_ID, text=msg)
    print(f"✅ Reminder sent at {hour}:00 — {msg}")

# 💡 Send Coding Tip
async def send_tip():
    bot = Bot(token=BOT_TOKEN)
    tip = random.choice(tips)
    msg = f"💡 *{tip['title']}*\n\n{tip['description']}"
    await bot.send_message(chat_id=USER_ID, text=msg, parse_mode='Markdown')
    print("✅ Tip sent:", tip['title'])

# 🌐 Keep alive server for UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "👋 Krishna's Reminder Bot is running!"

@app.route('/ping')
def ping():
    return "✅ Pong! Server is active."

def run_web():
    app.run(host='0.0.0.0', port=8080)

# 🔁 Start Everything
async def main():
    # Start Flask server in background thread
    threading.Thread(target=run_web).start()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder, 'cron', hour=9)
    scheduler.add_job(send_reminder, 'cron', hour=14)
    scheduler.add_job(send_reminder, 'cron', hour=19)
    scheduler.add_job(send_tip, 'interval', hours=2)  # For testing

    print("🤖 Krishna-CodeKarle-Bot chal raha hai bhai! Daant & Tips ready ho gyi.")
    scheduler.start()

    # Start Telegram bot
    application = Application.builder().token(BOT_TOKEN).build()
    await application.initialize()
    await application.start()
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
