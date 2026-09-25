import asyncio, os, threading, random, uuid
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from google import genai

TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CHANNEL = "@bdcapsoine"

client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Running"

last_captions = []
def generate_caption():
    global last_captions
    try:
        mood = random.choice(["গভীর রাতের কষ্ট", "হারানোর", "অপেক্ষার", "অভিমানের"])
        prompt = f"ID {uuid.uuid4()} সময় {datetime.now()} - তুমি {mood} নিয়ে @bdcapsoine এর জন্য বাংলায় একদম নতুন ৪ লাইনের স্যাড ক্যাপশন লেখো। আগেরগুলো {last_captions[-3:]} এর সাথে মিলবে না। শেষে মুড বুঝে ২টা ইমোজি দিবে 🥀💔😢🌙❤️"
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt, config={'temperature': 1.1})
        text = res.text.strip()
        last_captions.append(text)
        if len(last_captions) > 10: last_captions.pop(0)
        return text
    except Exception as e:
        print(e)
        return f"তোমায় আজও ভুলতে পারিনি। 🥀💔 {random.randint(1,99)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ বট চালু আছে ভাই। আমি প্রতি ৩০ মিনিট পর পর চ্যানেলে পোস্ট করছি।")

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # তোমার কথার উত্তর দেয়া বন্ধ
    await update.message.reply_text("✅ আমি চালু আছি ভাই, চ্যানেলে পোস্ট করছি।")

async def auto_post(app_bot):
    while True:
        try:
            caption = await asyncio.to_thread(generate_caption)
            await app_bot.bot.send_message(chat_id=CHANNEL, text=caption)
            print("Posted:", caption)
        except Exception as e:
            print(e)
        await asyncio.sleep(1800)

async def main_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, any_message))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    asyncio.create_task(auto_post(application))
    while True:
        await asyncio.sleep(3600)

def run_bot():
    asyncio.run(main_bot())

threading.Thread(target=run_bot, daemon=True).start()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
