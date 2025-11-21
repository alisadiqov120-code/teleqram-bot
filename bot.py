import os
import telebot
import psycopg2

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DATABASE_URL")

bot = telebot.TeleBot(BOT_TOKEN)

#DB bağlantısı
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Cədvəl yaradılır (əgər yoxdursa)
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age TEXT,
    profession TEXT,
    experience TEXT,
    contact TEXT
);
""")
conn.commit()

# Qeydiyyat mərhələsi üçün yaddaş
user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📌 Qeydiyyat", "🔍 Axtarış")
    bot.send_message(message.chat.id, "Salam! Menü seç:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "📌 Qeydiyyat")
def register_start(message):
    user_state[message.chat.id] = {"step": "name"}
    bot.send_message(message.chat.id, "Adınızı yazın:")


@bot.message_handler(func=lambda m: m.text == "🔍 Axtarış")
def search_start(message):
    user_state[message.chat.id] = {"step": "search"}
    bot.send_message(message.chat.id, "Peşə adı yazın (məs: dərzi):")


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    chat_id = message.chat.id

    # istifadəçi qeydiyyatdadırsa
    if chat_id in user_state:
        step = user_state[chat_id]["step"]

        if step == "name":
            user_state[chat_id]["name"] = message.text
            user_state[chat_id]["step"] = "age"
            bot.send_message(chat_id, "Yaşınızı yazın:")

        elif step == "age":
            user_state[chat_id]["age"] = message.text
            user_state[chat_id]["step"] = "profession"
            bot.send_message(chat_id, "Peşəniz:")

        elif step == "profession":
            user_state[chat_id]["profession"] = message.text
            user_state[chat_id]["step"] = "experience"
            bot.send_message(chat_id, "Stajınız:")

        elif step == "experience":
            user_state[chat_id]["experience"] = message.text
            user_state[chat_id]["step"] = "contact"
            bot.send_message(chat_id, "Əlaqə məlumatı (mobil və ya username):")

        elif step == "contact":
            user_state[chat_id]["contact"] = message.text

            data = user_state[chat_id]
            # DB-yə yaz
            cur.execute("""
                INSERT INTO users (name, age, profession, experience, contact)
                VALUES (%s, %s, %s, %s, %s)
            """, (data["name"], data["age"], data["profession"], data["experience"], data["contact"]))
            conn.commit()

            bot.send_message(chat_id, "✔ Qeydiyyat tamamlandı!")
            del user_state[chat_id]

        elif step == "search":
            profession = message.text.lower()
            cur.execute("SELECT name, age, profession, experience, contact FROM users WHERE profession ILIKE %s", (profession,))
            results = cur.fetchall()

            if len(results) == 0:
                bot.send_message(chat_id, "❌ Heç nə tapılmadı.")
            else:
                text = "🔍 Nəticələr:\n\n"
                for r in results:
                    text += f"👤 {r[0]}\n📌 Peşə: {r[2]}\n⏳ Staj: {r[3]}\n📞 Əlaqə: {r[4]}\n---\n"
                bot.send_message(chat_id, text)

            del user_state[chat_id]


bot.polling()
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot işləyir"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    bot.polling(non_stop=True)
    app.run(host="0.0.0.0", port=port)
