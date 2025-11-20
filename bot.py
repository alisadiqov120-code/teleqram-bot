import os
import telebot

# TOKEN Environment-dan oxunur
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

users = [
    {
        "name": "Ali",
        "profession": "programmer",
        "experience": "2 il",
        "contact": "@ali123",
        "photos": []
    }
]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salam! Axtarmaq istədiyin peşəni yaz:")

@bot.message_handler(func=lambda m: True)
def search(message):
    query = message.text.lower()
    found = [u for u in users if query in u["profession"].lower()]

    if found:
        for u in found:
            msg = (
                f"Ad: {u['name']}\n"
                f"Peşə: {u['profession']}\n"
                f"Təcrübə: {u['experience']}\n"
                f"Əlaqə: {u['contact']}"
            )
            bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, "Heç kim tapılmadı.")

bot.infinity_polling()
