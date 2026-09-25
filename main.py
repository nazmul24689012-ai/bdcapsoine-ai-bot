import asyncio, random, os
from telegram import Bot

TOKEN = os.environ.get("BOT_TOKEN") # Render এ BOT_TOKEN নামে Env বসাবে
CHANNEL = "@bdcapsoine"
bot = Bot(8621291963:AAGABywtHT5Lm7Xvy_wXw5TIEe-jv102cKk)

lines_pool = [
    "ভালোবাসা কখনো পুরানো হয় না, মানুষ বদলে যায়",
    "তোমাকে ভালোবাসাটা আমার অভ্যাস হয়ে গেছে",
    "মায়া বড় খারাপ জিনিস, ছাড়তেও দেয় না",
    "তোমার মায়ায় আটকে গেছি আজও",
    "আবেগগুলো আজকাল লুকিয়েই রাখি",
    "আবেগ বেশি দেখালে মানুষ সস্তা ভাবে",
    "একটু আদর, একটু যত্ন, এটুকুই তো চাওয়া",
    "যত্নে রাখলে সম্পর্ক সুন্দর থাকে",
    "তোমার মমতার কাছে আমি বারবার হেরে যাই",
    "কষ্টগুলো কাউকে দেখানো যায় না",
    "দুঃখটা এখন অভ্যাস হয়ে গেছে",
    "হাসি মুখে কষ্ট লুকানোর অভিনয়টা শিখে গেছি",
    "তোমাকে ভীষণ মনে পড়ছে আজ",
    "দূরে আছো বলেই কি ভুলে যাবো",
    "মনে পড়লেই বুকের ভেতরটা কেমন করে ওঠে",
    "যেখানে সম্মান নেই সেখানে ভালোবাসা থাকে না",
    "তোমার স্নেহটুকুই আমার সবচেয়ে বড় পাওয়া",
    "ভালোবাসলে আগলে রাখতে হয়, অবহেলায় নয়",
    "অপেক্ষা সুন্দর যদি মানুষটা সঠিক হয়"
]
endings = ["ভালো থেকো, যেখানেই থাকো। 🖤","ফিরে এসো, অপেক্ষায় আছি। ❤️","একদিন সব ঠিক হয়ে যাবে ইনশাআল্লাহ। ✨","থেকে গেলে যত্ন করতাম। 🥀"]

posted = set()
def generate_caption():
    while True:
        line_count = random.choice([4,5,6,7,8])
        selected = random.sample(lines_pool, line_count-1)
        caption = "\n".join([f"{l}।" for l in selected]) + f"\n\n{random.choice(endings)}"
        if caption not in posted:
            posted.add(caption)
            return caption

async def auto_post():
    while True:
        caption = generate_caption()
        try:
            await bot.send_message(chat_id=CHANNEL, text=caption)
            print(f"Posted {len(caption.splitlines())} lines")
        except Exception as e:
            print(e)
        await asyncio.sleep(900) # ১৫ মিনিট

asyncio.run(auto_post())
