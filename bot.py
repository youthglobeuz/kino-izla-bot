import time
time.sleep(3)
import telebot
from telebot import types
import requests
import time

BOT_TOKEN = "8374261818:AAHQ7Xvf-toUWxT5ipQrRhVrD-PmBmDDz-s"
CHANNEL_USERNAME = "@youthglobexba"   # asosiy kanal
MOVIE_CHANNEL = "@kiiinoIzla"    # kinolar kanali

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
        "💼 Eng ishonchli va litsenziyaga ega Xususiy Bandlik Agentliklari — bir joyda!\n"
        "Endi har birini alohida izlab yurish shart emas — faqat 1 bosishda eng faol va ishonchli XBA kanallariga a’zo bo‘ling! 🔥\n\n"
        "🌍 Ish topish — oson, tez va xavfsiz!\n\n"
        "👇 Quyidagi havolani bosing va tanlovni o‘zingiz qiling:\n"
        "➡️ 👉 [A’zo bo‘lish uchun bosing](https://t.me/addlist/hY66mxmsU3cwOTRi)!", 
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
            f"❌ Siz hali obuna bo‘lmadingiz.\nIltimos, kanalga obuna bo‘ling va qayta urinib ko‘ring 👇\n{CHANNEL_USERNAME}"
        )

# 🔹 Kino kodi orqali kino yuborish
@bot.message_handler(func=lambda m: m.text.startswith("#"))
def send_movie(message):
    code = message.text.strip()

    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"❌ Iltimos, avval {CHANNEL_USERNAME} kanaliga obuna bo‘ling.")
        return

    # 🔸 Kodga mos kino ID lar
    movies = {
        "#104": 3,
        "#1102": 4,
        "#1105": 5,
        "#843": 6,
        "#1212": 7,
        "#16": 8,
        "#9": 9,
        "#1315": 10,
        "#10": 11,
        "#24": 12,
        "#26": 13,
        "#25": 14,
        "#27": 15,
        "#105": 16,
        "#1200": 17,
        "#106": 18,
        "#250": 19,
        "#2019": 20,
        "#219": 21,
        "#404": 22,
        "#270": 23,
        "#390": 24,
        "#395": 25,
        "#398": 26,
        "#410": 27,
        "#444": 28,
        "#408": 29,
        "#256": 30,
        "#999": 31, 
"#898": 32,
 "#598": 33,
    }

    if code in movies:
        try:
            bot.copy_message(message.chat.id, MOVIE_CHANNEL, movies[code])
        except Exception as e:
            bot.send_message(
                message.chat.id,
                  "⚠️ Noto‘g‘ri kod. Iltimos, to‘g‘ri kino kodini kiriting (masalan: #999)"
            )
            print("Xatolik:", e)
    else:
        bot.send_message(
            message.chat.id,
            "⚠️ Noto‘g‘ri kod. Iltimos, to‘g‘ri kino kodini kiriting (masalan: #999)"
        )

# 🔹 Botni ishga tushirish
if __name__ == "__main__":
    time.sleep(3)
    print("🤖 Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)

