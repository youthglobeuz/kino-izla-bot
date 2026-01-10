import os
import telebot
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ================= ENV VARIABLES =================
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Telegram bot token
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")  # @xorijda_ish_elonlari
SHEET_NAME = os.environ.get("SHEET_NAME")  # Google Sheet nomi

# ================= GOOGLE SHEETS =================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# credentials.json faylni loyihaga joylang
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# ================= TELEGRAM BOT =================
bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\n\n"
        "Ish yarmarkasida ishtirok etish uchun ro‘yxatdan o‘ting.\n\n"
        "Iltimos, to‘liq ismingizni kiriting 👇"
    )
    bot.register_next_step_handler(message, get_name)

# ================= NAME =================
def get_name(message):
    user_data[message.chat.id] = {
        "name": message.text.strip(),
        "telegram_id": message.from_user.id,
        "username": message.from_user.username
    }

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True))

    bot.send_message(
        message.chat.id,
        "Rahmat!\nEndi telefon raqamingizni yuboring 👇",
        reply_markup=kb
    )

# ================= PHONE =================
@bot.message_handler(content_types=['contact'])
def get_phone(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number
    ask_location(message.chat.id)

# ================= LOCATION =================
def ask_location(chat_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    locations = [
        "Toshkent shahar", "Toshkent viloyati", "Andijon viloyati", "Fargona viloyati",
        "Namangan viloyati", "Sirdaryo viloyati", "Jizzah viloyati", "Samarqand viloyati",
        "Buhoro viloyati", "Navoi viloyati", "Horazm viloyati", "Qoraqalpogiston Respublikasi",
        "Qashqadaryo viloyati", "Surhondaryo viloyati"
    ]
    for loc in locations:
        kb.add(types.KeyboardButton(loc))

    msg = bot.send_message(
        chat_id,
        "Iltimos, qaysi hududdan ekanligingizni tanlang 👇",
        reply_markup=kb
    )
    bot.register_next_step_handler(msg, save_location)

# ================= SAVE LOCATION =================
def save_location(message):
    valid_locations = [
        "Toshkent shahar", "Toshkent viloyati", "Andijon viloyati", "Fargona viloyati",
        "Namangan viloyati", "Sirdaryo viloyati", "Jizzah viloyati", "Samarqand viloyati",
        "Buhoro viloyati", "Navoi viloyati", "Horazm viloyati", "Qoraqalpogiston Respublikasi",
        "Qashqadaryo viloyati", "Surhondaryo viloyati"
    ]

    if message.text not in valid_locations:
        bot.send_message(
            message.chat.id,
            "❌ Iltimos, faqat berilgan ro‘yxatdan tanlang."
        )
        ask_location(message.chat.id)
        return

    user_data[message.chat.id]["location"] = message.text

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "📢 Kanalga obuna bo‘lish",
        url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
    ))
    kb.add(types.InlineKeyboardButton(
        "✅ Obunani tekshirish",
        callback_data="check_sub"
    ))

    bot.send_message(
        message.chat.id,
        "Ish yarmarkasida ishtirok etish uchun kanalga obuna bo‘ling 👇",
        reply_markup=kb
    )

# ================= CHECK SUB =================
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, call.from_user.id).status

        if status in ["member", "administrator", "creator"]:
            save_to_sheet(call.message.chat.id)
            bot.answer_callback_query(call.id, "Tasdiqlandi ✅")
            bot.send_message(
                call.message.chat.id,
                "✅ Obuna tasdiqlandi!\n\n"
                "Siz Ish yarmarkasiga kirishingiz mumkin."
            )
        else:
            bot.answer_callback_query(call.id, "❌ Obuna topilmadi")
            bot.send_message(
                call.message.chat.id,
                "❌ Avval kanalga obuna bo‘ling va qayta tekshiring."
            )

    except Exception as e:
        bot.send_message(
            call.message.chat.id,
            f"❌ Tekshirishda xatolik yuz berdi.\n{str(e)}"
        )

# ================= SAVE TO SHEET =================
def save_to_sheet(chat_id):
    data = user_data.get(chat_id)
    if not data:
        return

    sheet.append_row([
        data.get("name"),
        data.get("phone"),
        data.get("location"),
        data.get("telegram_id"),
        data.get("username"),
        "YES",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])

# ================= RUN BOT =================
bot.infinity_polling()
