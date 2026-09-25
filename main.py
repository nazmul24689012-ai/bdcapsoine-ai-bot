import asyncio, random, os, threading
from flask import Flask
from telegram import Bot

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL = "@bdcapsoine"
bot = Bot(token=TOKEN)

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

async def auto_post():
    while True:
        try:
            await bot.send_message(chat_id=CHANNEL, text=generate_caption())
        except Exception as e:
            print(e)
        await asyncio.sleep(900) # 15 min

def run_bot():
    asyncio.run(auto_post())

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
