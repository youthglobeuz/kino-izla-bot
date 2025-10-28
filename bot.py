import telebot
from telebot import types
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_USERNAME = "@youthglobexba"

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data='check_sub')
    markup.add(btn)

    text = (
        f"🎬 Salom, {user.first_name}!\n\n"
        f"To‘liq filmlarni tomosha qilish uchun avval bizning asosiy kanalimizga obuna bo‘ling 👇\n\n"
        f"💼 Eng ishonchli va litsenziyaga ega Xususiy Bandlik Agentliklari — bir joyda!\n\n"
        f"Endi har birini alohida izlab yurish shart emas — faqat 1 bosishda 10 ta eng faol va ishonchli XBA kanallariga a’zo bo‘ling! 🔥\n\n"
        f"🌍 Ish topish — oson, tez va xavfsiz!\n\n"
        f"👇 Quyidagi havolani bosing va tanlovni o‘zingiz qiling:\n"
        f"➡️ 👉 [A’zo bo‘lish uchun bosing](https://t.me/addlist/hY66mxmsU3cwOTRi)\n\n"
        f"✅ Obuna bo‘lgandan so‘ng, pastdagi tugmani bosing ⤵️"
    )

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def check_subscription(call):
    user_id = call.from_user.id
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            send_movie_menu(call.message)
        else:
            bot.answer_callback_query(
                call.id,
                "🚫 Siz hali kanalga obuna bo‘lmagansiz. Iltimos, obuna bo‘ling va qayta urinib ko‘ring.",
                show_alert=True
            )
    except Exception as e:
        bot.answer_callback_query(call.id, f"❗ Xatolik: {e}", show_alert=True)

def send_movie_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎥 Yangi kinolar", callback_data='new_movies'))
    markup.add(types.InlineKeyboardButton("📺 Seriallar", callback_data='series'))
    markup.add(types.InlineKeyboardButton("🔙 Chiqish", callback_data='exit'))

    bot.send_message(
        message.chat.id,
        "🎉 Tabriklaymiz! Siz kanalga muvaffaqiyatli obuna bo‘ldingiz.\n\n"
        "Quyidagi bo‘limlardan birini tanlang 👇",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in ['new_movies', 'series', 'exit'])
def handle_menu(call):
    if call.data == 'new_movies':
        bot.send_message(call.message.chat.id, "🎬 Yangi kinolar ro‘yxati tez orada joylanadi!")
    elif call.data == 'series':
        bot.send_message(call.message.chat.id, "📺 Seriallar bo‘limi hali tayyor emas, tez orada!")
    elif call.data == 'exit':
        bot.send_message(call.message.chat.id, "👋 Rahmat! Botdan chiqdiz.")

if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    bot.infinity_polling()
