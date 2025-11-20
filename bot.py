import telebot

BOT_TOKEN = '5623273219:AAHhpyv2TbE73Xephn...'  # <-- Öz tokenini tam yaz

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
    bot.send_message(message.chat.id, "Salam! Peşə adını yaz, uyğun mütəxəssisləri göstərim.")

@bot.message_handler(func=lambda m: True)
def search(message):
    query = message.text.lower()
    found = [u for u in users if query in u["profession"].lower()]

    if found:
        for u in found:
            msg = f"Ad: {u['name']}\nPeşə: {u['profession']}\nTəcrübə: {u['experience']}\nƏlaqə: {u['contact']}"
            bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, "Uyğun mütəxəssis tapılmadı.")

bot.polling()
