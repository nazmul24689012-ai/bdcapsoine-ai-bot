import asyncio, os, threading
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
    return "Bot is Running - AI Mode"

# AI দিয়ে মুড বুঝে ইমোজি সহ ক্যাপশন
def generate_caption():
    try:
        prompt = """
        তুমি @bdcapsoine চ্যানেলের জন্য বাংলায় ৪-৬ লাইনের একটি ইমোশনাল, স্যাড, রোমান্টিক ক্যাপশন লেখো।
        প্রত্যেকবার একদম নতুন ক্যাপশন লিখবে, আগেরটা কপি করবে না।

        নিয়ম:
        - ক্যাপশন যদি কষ্টের / ব্রেকআপ / একাকিত্বের হয় তাহলে শেষে 🥀 😔 💔 🖤 😢 😭 এইগুলো থেকে মানানসই ইমোজি দিবে
        - ভালোবাসা / মায়া / যত্নের হলে ❤️ 🥰 😘 🌸 🤍 দিবে
        - মনে পড়া / অপেক্ষা / রাত জাগা হলে 🌙 🥺 ✨ দিবে
        - ইমোজি দেখেই যেন কষ্টটা বোঝা যায়, ক্যাপশনের মুড অনুযায়ী ইমোজি দিবে।
        - ২-৩ টার বেশি ইমোজি দিবে না।
        """
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return res.text.strip()
    except Exception as e:
        print(f"Caption Error: {e}")
        return "তোমার মায়ায় আজও আটকে আছি।\nভুলতে পারিনি তোমায়।\n\nভালো থেকো যেখানেই থাকো। 🥀💔"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("চালু আছি ভাই ✅\nএখন থেকে AI মুড বুঝে ইমোজি সহ ক্যাপশন দিবে।")

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        if not client:
            await update.message.reply_text("ভাই GEMINI_API_KEY পাচ্ছি না Render এ।")
            return
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"CHAT ERROR: {e}")
        await update.message.reply_text(f"এরর হচ্ছে ভাই: {e}")

async def auto_post(app_bot):
    while True:
        try:
            caption = await asyncio.to_thread(generate_caption)
            await app_bot.bot.send_message(chat_id=CHANNEL, text=caption)
            print(f"Posted: {caption}")
        except Exception as e:
            print(f"Post Error: {e}")
        await asyncio.sleep(900)  # 15 মিনিট

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
