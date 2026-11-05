import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from flask import Flask
import threading

# Tagall wale module ko import karna
from tagall import setup_tagall
from session_gen import setup_session_gen


# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render ke liye Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    mention_link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
    welcome_message = f"Namaste {mention_link}! 🙏\nAapka is Telegram Bot par swagat hai."
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode='HTML'
    )

if __name__ == '__main__':
    # Flask server background thread mein chalana
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Apna Bot Token yahan dalein
    TOKEN = "9131427352:AAFsoDDckWrFkwP-Up7RIWeIxuLg84oIDLY"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # /start handler add karna
    application.add_handler(CommandHandler('start', start))
    
    # Tagall module ke saare handlers yahan attach ho jayenge
    setup_tagall(application)
    setup_session_gen(application)
    
    
    print("Bot aur Web Server successfully start ho chuke hain...")
    application.run_polling()
    
