import telebot
import json
import os

# === CONFIGURATION ===
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
MOVIE_DATA = {
    "inception": {
        "channel": "@yourmovievault",  # replace with your channel username
        "message_id": 5  # replace with your message ID
    }
}
DATA_FILE = "data.json"

# === INIT BOT ===
bot = telebot.TeleBot(BOT_TOKEN)

# === Load requested users ===
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        requested = json.load(f)
else:
    requested = {}

# === Command Handler ===
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = str(message.chat.id)
    args = message.text.split()
    
    if len(args) < 2:
        bot.reply_to(message, "Get movie links from our channel!")
        return

    movie_key = args[1]

    if user_id in requested and movie_key in requested[user_id]:
        bot.send_message(message.chat.id, "You've already accessed this content. Go to the channel for more!")
        return

    if movie_key not in MOVIE_DATA:
        bot.send_message(message.chat.id, "Invalid or expired movie link.")
        return

    movie = MOVIE_DATA[movie_key]
    try:
        bot.forward_message(chat_id=message.chat.id, from_chat_id=movie["channel"], message_id=movie["message_id"])
        
        # Record access
        requested.setdefault(user_id, []).append(movie_key)
        with open(DATA_FILE, "w") as f:
            json.dump(requested, f)
            
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

# === Start polling ===
print("Bot is running...")
bot.infinity_polling()
