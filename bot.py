import telebot
from telebot import types
import requests
import os

BOT_TOKEN = os.getenv("8374261818:AAHQ7Xvf-toUWxT5ipQrRhVrD-PmBmDDz-s")
CHANNEL_USERNAME = os.getenv("yangi_kino_izla")  # example: @MyMovieChannel
ADMIN_ID = os.getenv("5571406870")  # your Telegram user ID

bot = telebot.TeleBot(BOT_TOKEN)

def is_subscribed(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    join_btn = types.InlineKeyboardButton("✅ I Joined", callback_data="check_join")
    markup.add(join_btn)
    bot.send_message(
        message.chat.id,
        f"🎬 Hello {message.from_user.first_name}!\n\nPlease join our movie channel first to continue:\n👉 {CHANNEL_USERNAME}",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_check(call):
    if is_subscribed(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Great! You’ve joined.\nNow send the *movie code* (for example: #001)", parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, f"❌ You haven’t joined yet.\nPlease join {CHANNEL_USERNAME} and try again.")

@bot.message_handler(func=lambda message: message.text.startswith("#"))
def send_movie(message):
    code = message.text.strip()
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"❌ You must join {CHANNEL_USERNAME} to get movies.")
        return

    # Example: match code manually with message IDs
    movie_dict = {
        "#001": 10,  # replace 10 with actual message ID in your channel
        "#002": 15,  # etc.
    }

    if code in movie_dict:
        bot.forward_message(message.chat.id, CHANNEL_USERNAME, movie_dict[code])
    else:
        bot.send_message(message.chat.id, "⚠️ Invalid movie code. Please try again.")

bot.infinity_polling()
