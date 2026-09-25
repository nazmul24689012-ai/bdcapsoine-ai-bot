import os, random, time, threading
from flask import Flask
from google import genai
from telegram import Bot

app = Flask(__name__)
@app.route('/')
def home(): return "Bot @bdcapsoine is Running"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = Bot(token=BOT_TOKEN)

TOPICS = ["ছেড়ে যাওয়া", "ধোঁকা খাওয়া", "না পাওয়া ভালোবাসা", "বেকার বলে ছেড়ে যাওয়া", "অন্যের হয়ে যাওয়া", "ব্লক", "৩ বছরের সম্পর্ক", "মিথ্যা ভালোবাসা", "একাকিত্ব", "মাঝরাতে কান্না", "পুরনো মেসেজ", "ভুলতে না পারা", "অপেক্ষা", "অবহেলা", "স্মৃতি"]

def make_post():
    topic = random.choice(TOPICS)
    prompt = f"""
    বিষয়: {topic}
    তুমি ২টা অংশ দেবে:
    STORY: এই বিষয়ে বাস্তব ব্রেকআপের মতো বড় গল্প, প্রতিটা বাক্য আলাদা লাইনে।
    CAPTION: গল্প অনুযায়ী ১-২ লাইনের ইমোশনাল ক্যাপশন + ইমোজি
    """
    res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    txt = res.text
    try:
        story = txt.split("CAPTION:")[0].replace("STORY:","").strip()
        caption = txt.split("CAPTION:")[1].strip()
    except:
        story = txt
        caption = "ভালোবাসা সুন্দর যদি মানুষটা সঠিক হয় 🥀💔"

    lines = [l.strip() for l in story.split('\n') if l.strip()!='']
    designed = [f"{random.choice(['>','•','—','›'])} {l}" for l in lines]
    final = "\n\n".join(designed) + f"\n\n\n{caption}\n\n@bdcapsoine"
    return final

def run_bot():
    try:
        bot.send_message(chat_id=CHANNEL_ID, text="✅ Bot সফলভাবে চালু হয়েছে @bdcapsoine\nএবার থেকে AI গল্প পোস্ট দেবে...")
        print("Test message sent!")
    except Exception as e:
        print(f"Test message failed: {e}")

    while True:
        try:
            post = make_post()
            bot.send_message(chat_id=CHANNEL_ID, text=post[:4000])
            print("AI Post Sent!")
            # পরের পোস্ট ২০ থেকে ৫০ মিনিট পর এলোমেলো
            sleep_time = random.choice([20,27,33,38,45,52]) * 60
            # দিনে ২-৩ টা বড় গল্পের জন্য মাঝে মাঝে লম্বা বিরতি
            if random.random() < 0.3:
                sleep_time = random.randint(7,10)*3600 + random.randint(5,55)*60

            print(f"Next in {sleep_time/60:.1f} min")
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
