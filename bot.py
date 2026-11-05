import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging setup karna taaki errors ya status console par dikhein
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # User ka first name nikalna
    user_name = update.effective_user.first_name
    
    # Welcome message banana
    welcome_message = f"Namaste {user_name}! 🙏\nAapka is Telegram Bot par swagat hai. Main aapki kya madad kar sakta hoon?"
    
    # User ko message bhejna
    await update.message.reply_text(welcome_message)

if __name__ == '__main__':
    # Yahan apna Telegram Bot Token dalein jo aapko BotFather se mila hai
    TOKEN = "9131427352:AAFsoDDckWrFkwP-Up7RIWeIxuLg84oIDLY"
    
    # Application build karein
    application = ApplicationBuilder().token(TOKEN).build()
    
    # /start command ke liye handler add karein
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    print("Bot successfully start ho chuka hai... (Band karne ke liye Ctrl+C dabayein)")
    
    # Bot ko run karein (polling start)
    application.run_polling()
  
