import telebot
from telebot import types

TOKEN = '7714405941:AAELHxpPvNc2uMeH2SBVnXqqD6r_wLqdCgQ'
CHANNEL_USERNAME = '@testforGoDxORion'

bot = telebot.TeleBot('7714405941:AAELHxpPvNc2uMeH2SBVnXqqD6r_wLqdCgQ')

users = {}
referrals = {}

def is_member(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()

    if not is_member(user_id):
        send_join_message(message)
        return

    if user_id not in users:
        users[user_id] = {'ref_by': None}
        if len(args) > 1:
            ref_by = int(args[1])
            if ref_by != user_id and ref_by in users:
                users[user_id]['ref_by'] = ref_by
                referrals[ref_by] = referrals.get(ref_by, 0) + 1
                bot.send_message(ref_by, f"Ek user aapke link se join hua!")

    bot.send_message(user_id, "Welcome to the Referral Bot!")
    bot.send_message(user_id, f"Aapka referral link:\nhttps://t.me/{{bot.get_me().username}}?start={{user_id}}")

def send_join_message(message):
    markup = types.InlineKeyboardMarkup()
    join = types.InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
    check = types.InlineKeyboardButton("I've Joined", callback_data="check_join")
    markup.add(join)
    markup.add(check)
    bot.send_message(message.chat.id, "Please join the channel first to use this bot:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    user_id = call.from_user.id
    if is_member(user_id):
        bot.send_message(user_id, "Thank you! You can now use the bot.")
        start(call.message)
    else:
        bot.send_message(user_id, "You haven't joined the channel yet. Please join first.")

@bot.message_handler(commands=['stats'])
def stats(message):
    user_id = message.from_user.id
    count = referrals.get(user_id, 0)
    bot.send_message(user_id, f"Total referrals: {count}")

bot.polling()
