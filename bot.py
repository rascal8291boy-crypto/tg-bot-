import logging
from telegram import Update, ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging setup karna
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # User ka object nikalna taaki uska ID aur Name mil sake
    user = update.effective_user
    user_name = user.first_name
    user_id = user.id
    
    # MarkdownV2 ya HTML ke zariye mention link banana taaki click karne par profile khule
    # Yahan hum HTML parse mode ka use kar rahe hain
    mention_link = f'<a href="tg://user?id={user_id}">{user_name}</a>'
    
    # Welcome message banana jisme clickable mention ho
    welcome_message = f"Namaste {mention_link}! 🙏\nAapka is Telegram Bot par swagat hai. Main aapki kya madad kar sakta hoon?"
    
    # Message bhejna aur parse_mode HTML set karna
    await update.message.reply_text(
        welcome_message, 
        parse_mode='HTML'
    )

if __name__ == '__main__':
    # Yahan apna Telegram Bot Token dalein jo BotFather se mila hai
    TOKEN = "9131427352:AAFsoDDckWrFkwP-Up7RIWeIxuLg84oIDLY"
    
    # Application build karein
    application = ApplicationBuilder().token(TOKEN).build()
    
    # /start command ke liye handler add karein
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    print("Bot successfully start ho chuka hai... (Band karne ke liye Ctrl+C dabayein)")
    
    # Bot ko run karein
    application.run_polling()
    
