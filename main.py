import asyncio
import random
import json
import os
import google.generativeai as genai
from telegram import Bot

# সেফ নিয়ম - কোডে সরাসরি Key নেই, Render থেকে আসবে
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("BOT_TOKEN বা GEMINI_API_KEY পাওয়া যায়নি! Render এ Environment Variable বসাও।")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = Bot(token=BOT_TOKEN)

TOPICS = [
    "ছেড়ে যাওয়া", "ধোঁকা খাওয়া", "না পাওয়া ভালোবাসা", "বেকার বলে ছেড়ে যাওয়া",
    "অন্যের হয়ে যাওয়া", "ব্লক করে দেওয়া", "৩ বছরের সম্পর্ক শেষ", "মিথ্যা ভালোবাসা",
    "একাকিত্ব", "মাঝরাতে কান্না", "পুরনো মেসেজ", "ভুলতে না পারা",
    "অপেক্ষা", "অবহেলা", "স্মৃতি", "কষ্ট", "বাস্তবতা", "হারিয়ে যাওয়া"
]

DESIGN_SYMBOLS = [">", "—", "-", "•", "›"]
POSTED_FILE = "posted.json"
posted_list = []
if os.path.exists(POSTED_FILE):
    try:
        with open(POSTED_FILE, "r", encoding="utf-8") as f:
            posted_list = json.load(f)
    except: posted_list = []

async def generate_story():
    topic = random.choice(TOPICS)
    prompt = f"""
    বিষয়: {topic} নিয়ে ফেসবুকে ভাইরাল হওয়া বাস্তব ব্রেকআপের গল্পের মতো করে একটি বড় গল্প লেখো। যত বড় পারো, কোনো লিমিট নেই। বাস্তব ও ইমোশনাল হতে হবে। আত্মহত্যায় উৎসাহ দেবে না। শুধু গল্প লেখো।
    """
    response = model.generate_content(prompt)
    text = response.text.strip()
    if text in posted_list:
        return await generate_story()
    
    lines = [f"{random.choice(DESIGN_SYMBOLS)} {l.strip()}" for l in text.split('\n') if l.strip()!=""]
    final_text = "\n".join(lines) + f"\n\n{random.choice(['💔','🥀','😔','💭','🌙','🖤','😢'])}"
    
    posted_list.append(text)
    with open(POSTED_FILE, "w", encoding="utf-8") as f:
        json.dump(posted_list[-500:], f, ensure_ascii=False, indent=2)
    return final_text

async def main():
    print(f"বট {CHANNEL_ID} এ চালু হয়েছে...")
    while True:
        try:
            story = await generate_story()
            await bot.send_message(chat_id=CHANNEL_ID, text=story)
            await asyncio.sleep(random.randint(25*60, 40*60))
        except Exception as e:
            print(f"এরর: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
