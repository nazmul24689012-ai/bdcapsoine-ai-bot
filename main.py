import asyncio, random, os, threading, google.generativeai as genai
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CHANNEL = "@bdcapsoine"

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running"

lines_pool = [
    "ভালোবাসা কখনো পুরানো হয় না, মানুষ বদলে যায়",
    "তোমাকে ভালোবাসাটা আমার অভ্যাস হয়ে গেছে",
    "মায়া বড় খারাপ জিনিস, ছাড়তেও দেয় না",
    "তোমার মায়ায় আটকে গেছি আজও",
    "আবেগগুলো আজকাল লুকিয়েই রাখি",
    "একটু আদর, একটু যত্ন, এটুকুই তো চাওয়া",
    "যত্নে রাখলে সম্পর্ক সুন্দর থাকে",
    "তোমার মমতার কাছে আমি বারবার হেরে যাই",
    "কষ্টগুলো কাউকে দেখানো যায় না",
    "দুঃখটা এখন অভ্যাস হয়ে গেছে",
    "তোমাকে ভীষণ মনে পড়ছে আজ",
    "দূরে আছো বলেই কি ভুলে যাবো",
    "যেখানে সম্মান নেই সেখানে ভালোবাসা থাকে না",
    "তোমার স্নেহটুকুই আমার সবচেয়ে বড় পাওয়া"
]
endings = ["ভালো থেকো, যেখানেই থাকো। 🖤","ফিরে এসো, অপেক্ষায় আছি। ❤️","একদিন সব ঠিক হয়ে যাবে ইনশাআল্লাহ। ✨"]

def generate_caption():
    c = random.choice([4,5,6,7,8])
    sel = random.sample(lines_pool, c-1)
    return "\n".join([f"{l}।" for l in sel]) + f"\n\n{random.choice(endings)}"

# --- কথা বলার জন্য ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আমি চালু আছি ভাই ✅\nতোমার @bdcapsoine চ্যানেলে প্রতি ১৫ মিনিট পর পর অটো পোস্ট করছি। 🖤")

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        if GEMINI_KEY:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = await asyncio.to_thread(model.generate_content, user_text)
            reply = response.text
        else:
            reply = "ভাই GEMINI_API_KEY পাচ্ছি না, তাই উত্তর দিতে পারছি না।"
        await update.message.reply_text(reply)
    except Exception as e:
        print(e)
        await update.message.reply_text("একটু সমস্যা হচ্ছে ভাই, আবার বলো তো।")

async def auto_post(app_bot):
    while True:
        try:
            await app_bot.bot.send_message(chat_id=CHANNEL, text=generate_caption())
            print("Posted to channel")
        except Exception as e:
            print(e)
        await asyncio.sleep(900)

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
