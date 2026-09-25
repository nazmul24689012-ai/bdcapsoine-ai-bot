import os, random, time, threading
from flask import Flask
from google import genai
from telegram import Bot

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Running @bdcapsoine"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = Bot(token=BOT_TOKEN)

TOPICS = ["ছেড়ে যাওয়া", "ধোঁকা খাওয়া", "না পাওয়া ভালোবাসা", "বেকার বলে ছেড়ে যাওয়া", "অন্যের হয়ে যাওয়া", "ব্লক করে দেওয়া", "৩ বছরের সম্পর্ক শেষ", "মিথ্যা ভালোবাসা", "একাকিত্ব", "মাঝরাতে কান্না", "পুরনো মেসেজ", "ভুলতে না পারা", "অপেক্ষা", "অবহেলা", "স্মৃতি", "কষ্ট", "বাস্তবতা", "হারিয়ে যাওয়া"]
SYMBOLS = [">", "•", "—", "›"]

def get_ai_content(type_text):
    if type_text == "story":
        prompt = f"বিষয়: {random.choice(TOPICS)} - এই বিষয়ে বাস্তব জীবনের মতো অনেক বড়, ইমোশনাল ব্রেকআপ গল্প লেখো। প্রতিটা বাক্য আলাদা লাইনে লেখো।"
    else:
        prompt = f"বিষয়: {random.choice(TOPICS)} - এই বিষয়ে ১-২ লাইনের একটা ছোট, কষ্টের ক্যাপশন লেখো। সাথে ২টা ইমোজি দেবে। যেমন: ভালোবাসা সুন্দর যদি মানুষটা সঠিক হয় 🥀💔"

    res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    text = res.text.strip()
    
    # ডিজাইন: লাইন বাই লাইন গ্যাপ দিয়ে
    lines = [l.strip() for l in text.split('\n') if l.strip()!='']
    designed = [f"{random.choice(SYMBOLS)} {line}" for line in lines]
    final = "\n\n".join(designed)
    
    if type_text == "story":
        final += f"\n\n\n{random.choice(['💔','🥀','😔','🌙'])} @bdcapsoine"
    return final

def run_bot():
    story_count_today = 0
    last_story_time = 0
    while True:
        try:
            current_time = time.time()
            # ২৪ ঘন্টায় ২-৩টা গল্প, মানে ৮-১২ ঘন্টা পর পর
            should_post_story = (current_time - last_story_time > random.randint(8*3600, 12*3600)) and story_count_today < 3

            if should_post_story:
                post = get_ai_content("story")
                print("বড় গল্প পোস্ট হচ্ছে...")
                story_count_today += 1
                last_story_time = current_time
                sleep_next = random.randint(20, 50) * 60
            else:
                post = get_ai_content("caption")
                print("ক্যাপশন পোস্ট হচ্ছে...")
                # ক্যাপশনের টাইম এলোমেলো: ২০/৩০/৪০ মিনিট, বারবার একই না
                sleep_next = random.choice([20, 27, 33, 38, 45, 52]) * 60

            # বড় হলে ভেঙে পাঠাবে
            for i in range(0, len(post), 4000):
                bot.send_message(chat_id=CHANNEL_ID, text=post[i:i+4000])
                time.sleep(3)
            
            # ২৪ ঘন্টা পর রিসেট
            if current_time - last_story_time > 24*3600:
                story_count_today = 0

            print(f"পরের পোস্ট {sleep_next//60} মিনিট পর")
            time.sleep(sleep_next)

        except Exception as e:
            print(f"এরর: {e}")
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
