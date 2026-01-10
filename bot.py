


import os
import json
import telebot
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ================= ENV VARIABLES =================
# Render.com-da ENV variables yarating va ularni shu nomlar bilan qo'ying
BOT_TOKEN = os.environ.get("8532689265:AAGMA6pwWeNpzjD7LS9Jrb9fsn7xgJmySgA")
CHANNEL_USERNAME = os.environ.get("xorijda_ish_elonlari")
SHEET_NAME = os.environ.get("Xorijda ish yarmakasi lead")
GOOGLE_CREDENTIALS_JSON = os.environ.get("{"type":"service_account","project_id":"association-483913","private_key_id":"db7e2bac651c15add3bf711adacc671ca4c06ef5","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQD6EhMhMj7l1mbCmfp9CM47N0K+WsESW/CfKi1gQiDrT6B1W2E0aCN4pMzZtGkTURHudoBpUF45q2UuKt3QRkH8LoIIhLEEiSBfowpQyg8P5U0p+BnfFaGjmQP3H3Uy8e/XD/XTOrvx3V5cWMCQc30tlSLrNiFKf1QgdUEbzVpDmlc29R56J3SKuvj/i3CSJClTSDI9sw4yHTcayg77wDRpxSzIido5qjuw1DEZgWe47/PlsKaDvFkkhfqo/9cNZEpLzLnG7S1jBNETKAi/53Bvwoghuh5VRm/e86H1vF6BJFlkL6QpL7zlZxcGMOC/49Lg0emeZMBiD5WWbLf7vD2BAgMBAAECggEAQpYOfu/cnKF+wkFy19lA5LadsIcE0uklRJRb+b4R+uY8cRNQaj5yd3zWSP/HXMvg7PCj16b9N/jh262xW3RhvI77s931LqJ+ush0hjePVCm35r130hV18VRcoHBBajvOo6LNz51bjxblOcyuFaiSw9Dqt9u1eJs34N6n5AnFh6sp4EB3llH7/Hst6piP9v6uqIkB8qi6nOleJxCLdL6y32t2NPeOxhWM1nw8l1LamS5HjLhr5H+zbXRn59bt61IX6bwU+Vl+3j7qfvmkACq+/9p+Dho+ek4+ta4T9PMd0oimRtOboJwiOnTm86EFNqwPtkfi7oWbGMt15cJci+j6MwKBgQD96IlyQqxSItZCQyWmSjk1PlwSB2fECNa2qSmkAyBENR/GwfQ9A68At+wusDXAL1peiHSb4NrPkdLFlwQzHuVPYtg9gvXXRqbUoARHX1Py5d3IDDsi3isRSzEpZ5xXU2P1mRAZV46y1gPlauILKIlKJlcAISlRaNB85Jg6NsMymwKBgQD8IXHJAKSrDtncBfBgnJG6VG8ZtfcQmeXVF1RYjlZ9qthh600y+boF5x4kDmSs5hpWO0f1lfwRvQLNQuF3FOFLpFI5XRivgbQrUn1LY4OMhcz8dQ1tbc9meIU8bfPcHM7ZlkxJYTzjnanHt7lqKNUpsrQbh7afpn3lbUfFgmg0EwKBgF2EaitFV0ahQh0Bsjo/GDb+EtcpFxTi1IJOZ+HarOWyU1PXV+epFanEFB9WE1YHmtc6lwhalvzgjqrr5kYV2QuWMmLlezqg8Q1bKnhHKhpKg5cMujMrdN1XvnGrka+wLR7mE0HiN9KydJjo9vx5H6fJ2z1W+Wrcmf2GDHNUfCyFAoGBAOcTP9WYYVLlKYYda1EgLe83sxs9SlJMufeyifsfeOVzzxzvKrGtbnA6gcVJ67sKqNifPDQ4Ye1f7VFyGnGpEVLiJvmr+RPhK98ImwydB9OiTVyTatr/6TVg/7uCih0RygJhXUljdQqnVRNVrvk8syCkR61zlEx9qqS6oyzBd/9BAoGAbDJTzdi5NTPXiKcXzQG2zSEi7s7x2jnVvwfjjEe6ay/oiSd7M2uBpLYZxD3WaI+m3ZsM2z8JjoW3E4buhoKqD5ZGT6ZnNoaGHHBpM2YBsTgvnFj5zjR6df81mkNHmG8VAVzCkaRK2kWkFrPUovs2u7I5iIoK8/O4bLfWeZLoepc=","client_email":"association@association-483913.iam.gserviceaccount.com","client_id":"113836124134960305531","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/association%40association-483913.iam.gserviceaccount.com","universe_domain":"googleapis.com"}")  # Service account JSON bitta qatorda

# ================= TELEGRAM BOT =================
bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# ================= GOOGLE SHEETS =================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# JSON ni dict ga o'zgartiramiz
creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

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
        "name": message.text,
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

# ================= RUN =================
bot.infinity_polling()
