import telebot

BOT_TOKEN = "8523273219:AAHhpy2VHQT2bE73xeNgFHGA6SThaLIFfMk"

bot = telebot.TeleBot(BOT_TOKEN)

users = {
    1: {
        "name": "Ali",
        "profession": "programmer",
        "experience": "2 il",
        "contact": "@ali123",
        "photos": []
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salam! Peşə adını yazın:")

@bot.message_handler(func=lambda m: True)
def do_search(message):
    query = message.text.lower()
    found = [u for u in users.values() if u['profession'] == query]
    if found:
        for u in found:
            info = f"{u['name']} — {u['experience']} — {u['contact']}"
            bot.send_message(message.chat.id, info)
            for p in u['photos']:
                bot.send_photo(message.chat.id, p)
    else:
        bot.send_message(message.chat.id, "Bu sahə üzrə qeydiyyat tapılmadı.")

print("Bot is polling...")
bot.polling()
