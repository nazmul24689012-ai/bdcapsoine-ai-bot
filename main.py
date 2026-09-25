import asyncio, os, threading, random, uuid
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
    return "Bot is Running"

last_caption = ""

def generate_caption():
    global last_caption
    # ৬ থেকে ১২ লাইনের মধ্যে র‍্যান্ডম
    line_count = random.randint(6, 12)
    mood = random.choice(["গভীর রাতের কষ্ট", "হারিয়ে ফেলা ভালোবাসা", "অপেক্ষা", "অভিমান", "একাকিত্ব"])

    prompt = f"""
    তুমি {mood} নিয়ে বাংলায় ঠিক {line_count} লাইনের একটি নতুন স্যাড ক্যাপশন লেখো @bdcapsoine এর জন্য।
    আগের ক্যাপশন ছিল: "{last_caption}" - এটার সাথে যেন একটুও না মিলে।
    নিয়ম: কোনো সংখ্যা, ID, লাইন নম্বর লিখবে না। শুধু ক্যাপশন।
    শেষ লাইনে মুড বুঝে ২-৩টা ইমোজি দিবে। Ref: {uuid.uuid4()}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={'temperature': 1.3}
    )
    last_caption = response.text.strip()
    return last_caption

# বটে hi লিখলে রিপ্লাই
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ হ্যাঁ ভাই আমি চালু আছি, প্রতি ৩০ মিনিট পর পর AI দিয়ে নতুন ক্যাপশন দিচ্ছি।")

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ হ্যাঁ ভাই আমি চালু আছি, চিন্তা করো না।")

# ৩০ মিনিট পর পর অটো পোস্ট
async def auto_post(app_bot):
    while True:
        try:
            caption = await asyncio.to_thread(generate_caption)
            await app_bot.bot.send_message(chat_id=CHANNEL, text=caption)
            print("Posted new caption")
        except Exception as e:
            print("Gemini fail, skipping this time")
            print(e)
        await asyncio.sleep(1800) # 30 মিনিট

async def main_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, any_message))
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    asyncio.create_task(auto_post(application))
    while True:
        await asyncio.sleep(3600)
def run_bot():
    asyncio.run(main_bot())

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
