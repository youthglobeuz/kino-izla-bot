import time
time.sleep(3)
import telebot
from telebot import types
import requests

BOT_TOKEN = "8374261818:AAHQ7Xvf-toUWxT5ipQrRhVrD-PmBmDDz-s"
CHANNEL_USERNAME = "@youthglobexba"   # asosiy kanal (obuna bo‘lish shart)
MOVIE_CHANNEL = "@Yangi_kino_izla"   # kinolar saqlanadigan kanal

bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Obunani tekshirish funksiyasi
def is_subscribed(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    r = requests.get(url).json()
    status = r.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

# 🔹 /start buyrug‘i
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    join_btn = types.InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_join")
    markup.add(join_btn)

    bot.send_message(
        message.chat.id,
        f"🎬 Salom, {message.from_user.first_name}!\n\n"
        "To‘liq filmlarni tomosha qilish uchun avval bizning asosiy kanalimizga obuna bo‘ling 👇\n\n"
        "💼 Eng ishonchli va litsenziyaga ega Xususiy Bandlik Agentliklari — bir joyda!\n\n"
        "🌍 Quyidagi havolani bosing va tanlovni o‘zingiz qiling:\n"
        "➡️ 👉 [A’zo bo‘lish uchun bosing](https://t.me/c/3134720426/31)",
        parse_mode="Markdown",
        reply_markup=markup
    )

# 🔹 Obuna tekshirish callback
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_check(call):
    if is_subscribed(call.from_user.id):
        bot.send_message(
            call.message.chat.id,
            "✅ Tabriklaymiz! Siz kanalga muvaffaqiyatli obuna bo‘ldingiz.\n\n"
            "🎞 Endi kino kodini kiriting (masalan: #001)"
        )
    else:
        bot.send_message(
            call.message.chat.id,
            "❌ Siz hali obuna bo‘lmadingiz.\nIltimos, kanalga obuna bo‘ling va qayta urinib ko‘ring 👇\n"
            f"{CHANNEL_USERNAME}"
        )

# 🔹 Kino kodi qabul qilish
@bot.message_handler(func=lambda m: m.text.startswith("#"))
def send_movie(message):
    code = message.text.strip()

    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"❌ Iltimos, avval {CHANNEL_USERNAME} kanaliga obuna bo‘ling.")
        return

    # 🔸 Kodga mos kino ID lar
    movies = {
        "#001": 10,  # bu joyga haqiqiy kino post ID larini kiriting
        "#002": 15,
        "#003": 20
    }

    if code in movies:
        try:
            bot.forward_message(message.chat.id, MOVIE_CHANNEL, movies[code])
        except Exception as e:
            bot.send_message(message.chat.id, "⚠️ Kino topilmadi yoki kanalga botni admin qilib qo‘ymagansiz.")
            print(e)
    else:
        bot.send_message(message.chat.id, "⚠️ Noto‘g‘ri kod. Iltimos, to‘g‘ri kino kodini kiriting (masalan: #001)")

# 🔹 Botni ishga tushirish
if __name__ == "__main__":
    import time
    time.sleep(3)
    print("🤖 Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)
