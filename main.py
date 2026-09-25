import asyncio, random, os, threading
from flask import Flask
from telegram import Bot

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL = "@bdcapsoine"
bot = 8621291963:AAGABywtHT5Lm7Xvy_wXw5TIEe-jv102cKk

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running 24/7"

# ... তোমার বাকি সব কোড একই থাকবে ...
lines_pool = ["ভালোবাসা কখনো পুরানো হয় না","তোমাকে ভালোবাসাটা অভ্যাস","মায়া বড় খারাপ জিনিস","আবেগগুলো লুকিয়েই রাখি","একটু আদর একটু যত্ন","তোমার মমতার কাছে হেরে যাই","কষ্টগুলো দেখানো যায় না","দুঃখটা অভ্যাস হয়ে গেছে","তোমাকে ভীষণ মনে পড়ছে","দূরে আছো বলেই কি ভুলে যাবো","যেখানে সম্মান নেই সেখানে ভালোবাসা নেই","তোমার স্নেহটুকুই সবচেয়ে বড় পাওয়া"]

def generate_caption():
    return random.choice(lines_pool) + "।\n" + random.choice(lines_pool) + "।\n\nভালো থেকো। 🖤"

async def auto_post():
    while True:
        try:
            await bot.send_message(chat_id=CHANNEL, text=generate_caption())
        except Exception as e:
            print(e)
        await asyncio.sleep(900)

def run_bot():
    asyncio.run(auto_post())

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
