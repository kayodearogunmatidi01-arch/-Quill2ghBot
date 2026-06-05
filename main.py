import os
import telebot

# Retrieve the bot token from Render's environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

bot = telebot.TeleBot(BOT_TOKEN)

# This handler triggers whenever ANYONE sends /start to the bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Welcome to <b>QuillBot</b>!\n\n"
        "Your ultimate sports companion. Get instant live scores, breaking news, and "
        "match highlights delivered right here.\n\n"
        "Tap /start to choose your favorite teams and never miss a big moment!"
    )
    
    # send_message sends it back to the specific user who triggered it
    bot.send_message(chat_id=message.chat.id, text=welcome_text, parse_mode='HTML')

if __name__ == '__main__':
    print("QuillBot is spinning up... Press Ctrl+C to exit locally.")
    # infinity_polling keeps the bot running continuously
    bot.infinity_polling()
