import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging setup karna
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # User ka object nikalna
    user = update.effective_user
    user_name = user.first_name
    user_id = user.id
    
    # Clickable profile link ke liye HTML tag
    mention_link = f'<a href="tg://user?id={user_id}">{user_name}</a>'
    
    # Welcome message
    welcome_message = f"Namaste {mention_link}! 🙏\nAapka is Telegram Bot par swagat hai. Main aapki kya madad kar sakta hoon?"
    
    # Yahan parse_mode mein seedha 'HTML' string pass kar rahe hain
    await update.message.reply_text(
        welcome_message, 
        parse_mode='HTML'
    )

if __name__ == '__main__':
    # Yahan apna Telegram Bot Token dalein
    TOKEN = "9131427352:AAFsoDDckWrFkwP-Up7RIWeIxuLg84oIDLY"
    
    # Application build karein
    application = ApplicationBuilder().token(TOKEN).build()
    
    # /start command handler
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    print("Bot successfully start ho chuka hai...")
    
    # Bot ko run karein
    application.run_polling()
    
