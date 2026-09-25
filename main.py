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

def generate_caption():
    try:
        moods = ["হারানোর কষ্ট", "গভীর রাতের একাকিত্ব", "অপেক্ষা", "অভিমান", "না বলা ভালোবাসা", "প্রিয় মানুষকে মিস করা"]
        mood = random.choice(moods)
        line_count = random.randint(4, 10) # ৪ থেকে ১০ লাইনের মধ্যে র‍্যান্ডম
        
        prompt = f"""
        তুমি {mood} নিয়ে বাংলায় ঠিক {line_count} লাইনের একদম নতুন, ইউনিক স্যাড ক্যাপশন লেখো @bdcapsoine চ্যানেলের জন্য।
        শর্ত: কোনো সংখ্যা, ID, লাইন নাম্বার লিখবে না। শুধু ক্যাপশন দিবে।
        লাইন {line_count} টাই হতে হবে, কম বেশি না।
        শেষে মুড বুঝে ২টা ইমোজি দিবে (🥀💔😢🌙🖤🥺) - Ref: {uuid.uuid4()}
        """
        res = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
            config={'temperature': 1.2}
        )
        return res.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        fallback_list = [
            "তোমার সাথে কাটানো সময়গুলো আজও খুব মনে পড়ে।\nভুলতে চাই, কিন্তু পারি না।\nতুমি কি আমায় মনে রাখো?\nভালো থেকো তুমি। 🥀💔",
            "রাত যত গভীর হয়,\nতোমার অভাব তত বেশি বোঝা যায়।\nঘুম আসে না চোখে,\nশুধু তোমার স্মৃতি ভাসে।\nঅপেক্ষায় আছি আজও। 🌙😔",
            "অভিমান করে চলে গেলে তুমি।\nভেবেছিলে ফিরিয়ে আনবো।\nআমি অপেক্ষায় ছিলাম,\nতুমি আর ফিরলে না।\nশিখিয়ে গেলে একা বাঁচতে।\nতবুও ভালোবাসি তোমায়। 🖤🥺"
        ]
        return random.choice(fallback_list)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ আমি চালু আছি ভাই, প্রতি ৩০ মিনিট পর পর ৪-১০ লাইনের ক্যাপশন পোস্ট করছি।")

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ আমি চালু আছি ভাই, চ্যানেলে পোস্ট করছি।")

async def auto_post(app_bot):
    while True:
        try:
            caption = await asyncio.to_thread(generate_caption)
            await app_bot.bot.send_message(chat_id=CHANNEL, text=caption)
            print(f"Posted: {
