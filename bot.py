import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from flask import Flask
import threading

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Chota sa Flask app banana taaki Render URL par HTTP request aane par response mil sake
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    # Render jo PORT environment variable deta hai, us par app run karna
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name
    user_id = user.id
    
    mention_link = f'<a href="tg://user?id={user_id}">{user_name}</a>'
    welcome_message = f"Namaste {mention_link}! 🙏\nAapka is Telegram Bot par swagat hai. Main aapki kya madad kar sakta hoon?"
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode='HTML'
    )

if __name__ == '__main__':
    # Flask server ko ek alag background thread mein chalana
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Telegram Bot Token
    TOKEN = "9131427352:AAFsoDDckWrFkwP-Up7RIWeIxuLg84oIDLY"
    
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    print("Bot aur Web Server successfully start ho chuke hain...")
    application.run_polling()
    
