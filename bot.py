import telebot, requests, os
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # @youthglobexba
MOVIE_CHANNEL = os.getenv("MOVIE_CHANNEL")        # @Yangi_kino_izla
ADMIN_ID = os.getenv("ADMIN_ID")

bot = telebot.TeleBot(BOT_TOKEN)

def is_subscribed(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    res = requests.get(url).json()
    return res.get("result", {}).get("status") in ["member", "administrator", "creator"]

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ I Subscribed", callback_data="check"))
    bot.send_message(
        message.chat.id,
        f"🎬 Hello {message.from_user.first_name}!\n\nTo watch full movies, please first subscribe to our main channel 👇\n👉 {CHANNEL_USERNAME}",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if is_subscribed(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Great! Send the *movie code* (e.g. #001)", parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, f"❌ You haven’t joined {CHANNEL_USERNAME} yet. Please join and try again.")

@bot.message_handler(func=lambda m: m.text.startswith("#"))
def movie_code(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"❌ You must join {CHANNEL_USERNAME} first.")
        return
    movies = {"#001": 10, "#002": 15}  # Replace with your actual message IDs
    code = message.text.strip()
    if code in movies:
        bot.forward_message(message.chat.id, MOVIE_CHANNEL, movies[code])
    else:
        bot.send_message(message.chat.id, "⚠️ Invalid movie code.")

bot.infinity_polling()

