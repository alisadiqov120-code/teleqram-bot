import os
import telebot

# 🔹 Environment-dan token oxunur
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Token yoxdursa program dayansın və səbəbi logda görünsün
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment dəyişəni tapılmadı!")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# 🔹 Menyudakı istifadəçi məlumatı
users = [
    {
        "name": "Ali",
        "profession": "Programmer",
        "experience": "2 il",
        "contact": "@ali123",
        "photos": []
    }
]

# 🔹 /start komandasını qarşılayır
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Haqqımda", "Əlaqə")
    markup.row("Portfolio", "Təcrübə")
    bot.send_message(
        message.chat.id,
        "Salam! Mənim haqqımda məlumat almaq üçün seçim et:",
        reply_markup=markup
    )

# 🔹 Menyu cavablandırma
@bot.message_handler(func=lambda m: True)
def menu(message):
    text = message.text.lower()

    if text == "haqqımda":
        bot.send_message(
            message.chat.id,
            f"👤 Ad: {users[0]['name']}\n💼 Peşə: {users[0]['profession']}"
        )

    elif text == "təcrübə":
        bot.send_message(
            message.chat.id,
            f"📌 Təcrübə: {users[0]['experience']}"
        )

    elif text == "əlaqə":
        bot.send_message(
            message.chat.id,
            f"📨 Əlaqə: {users[0]['contact']}"
        )

    elif text == "portfolio":
        bot.send_message(
            message.chat.id,
            f"📁 Portfolio hələ əlavə edilməyib."
        )

    else:
        bot.send_message(message.chat.id, "❓ Tanınmayan seçim.")


# 🔹 Botu işə salır (worker üçün)
print("🚀 Bot işə düşdü...")
bot.infinity_polling()
