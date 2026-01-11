import telebot
from telebot import types
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = "@migratsiya"

bot = telebot.TeleBot(BOT_TOKEN)


def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id

    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "📢 Kanalga obuna bo‘lish",
                url="https://t.me/migratsiya"
            )
        )
        markup.add(
            types.InlineKeyboardButton(
                "✅ Obunani tekshirish",
                callback_data="check_sub"
            )
        )

        bot.send_message(
            message.chat.id,
            "❗ Davom etish uchun avval kanalga obuna bo‘ling:\n\n👉 @migratsiya",
            reply_markup=markup
        )
    else:
        send_form_link(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id

    if is_subscribed(user_id):
        bot.answer_callback_query(call.id, "✅ Obuna tasdiqlandi")
        send_form_link(call.message.chat.id)
    else:
        bot.answer_callback_query(
            call.id,
            "❌ Siz hali kanalga obuna bo‘lmadingiz",
            show_alert=True
        )


def send_form_link(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📝 Arizani to‘ldirish",
            url="https://youthglobe.uz/xorijda-ish-yarmarkasi/"
        )
    )

    bot.send_message(
        chat_id,
        "✅ Rahmat!\n\n"
        "Quyidagi havolani to‘ldiring va "
        "Xorijda ish mehnat yarmarkasiga kirishingiz mumkin 👇",
        reply_markup=markup
    )


bot.infinity_polling()
