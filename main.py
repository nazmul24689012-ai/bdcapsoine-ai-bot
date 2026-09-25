import asyncio, random, os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from google import genai

TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CHANNEL = "@bdcapsoine"

client = None
if GEMINI_KEY:
    client = genai.Client(api_key=GEMINI_KEY)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running"

# AI দিয়ে ক্যাপশন বানানোর ফাংশন
def generate_caption():
    try:
        if not client:
            return "তোমাকে ভীষণ মনে পড়ছে আজ।\n\nভালো থেকো, যেখানেই থাকো। 🖤"

        prompt = """
        তুমি @bdcapsoine চ্যানেলের জন্য বাংলায় ৪-৬ লাইনের একটি ইমোশনাল, স্যাড, রোমান্টিক ক্যাপশন লেখো।
        প্রত্যেক লাইন ছোট হবে।
        ভালোবাসা, মায়া, যত্ন, অভিমান, মনে পড়া, সম্মান নিয়ে লিখবে।
        শেষে একটা সুন্দর ইমোজি সহ ending দিবে যেমন: ভালো থেকো যেখানেই থাকো 🖤 বা ফিরে এসো অপেক্ষায় আছি ❤️
        একই কথা বারবার লিখবে না, প্রতিবার নতুন লিখবে।
        """
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Caption Error: {e}")
        return "মায়া বড় খারাপ জিনিস, ছাড়তেও দেয় না।\nতোমার মায়ায় আটকে গেছি আজও।\n\nভালো থেকো, যেখানেই থাকো। 🖤"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আমি চালু আছি ভাই ✅\nতোমার @bdcapsoine চ্যানেলে প্রতি ১৫ মিনিট পর পর AI দিয়ে অটো পোস্ট করছি। 🖤")

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        if not client:
            await update.message.reply_text("ভাই GEMINI_API_KEY পাচ্ছি না।")
            return
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.0-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"GEMINI ERROR: {e}")
        await update.message.reply_text(f"এরর হচ্ছে: {e}")

async def auto_post(app_bot):
    while True:
        try:
            caption = await asyncio.to_thread(generate_caption)
            await app_bot.bot.send_message(chat_id=CHANNEL, text=caption)
            print("AI Caption Posted")
        except Exception as e:
            print(e)
        await asyncio.sleep(900) # 15 min

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
