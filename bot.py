import logging
import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
from tagall import setup_tagall
#from session_gen import setup_session_gen



# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Render ke liye Flask server
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is alive and running!"


# Main Menu Layout (Reusable function)
def get_main_menu_keyboard():
  return [
      [InlineKeyboardButton("💡 HELP & COMMANDS", callback_data="help_menu")],
      [
          InlineKeyboardButton("🔑 GEN SESSION", callback_data="gen_session"),
          InlineKeyboardButton("🏷️ TAGALL INFO", callback_data="tagall_info"),
      ],
  ]


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user
  mention_link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'

  welcome_message = (
      f"Namaste {mention_link}! 🙏\n"
      "Aapka is Telegram Bot par swagat hai. Niche diye gaye button par click karke"
      " commands ki jankari lein:"
  )

  reply_markup = InlineKeyboardMarkup(get_main_menu_keyboard())

  # Check karega ki yeh command se aaya hai ya callback (Back button) se
  if update.message:
    await update.message.reply_text(
        welcome_message, reply_markup=reply_markup, parse_mode="HTML"
    )
  elif update.callback_query:
    query = update.callback_query
    await query.edit_message_text(
        welcome_message, reply_markup=reply_markup, parse_mode="HTML"
    )


# Button click handler with Back Button support
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  if query.data == "back_to_home":
    user = query.from_user
    mention_link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
    welcome_message = (
        f"Namaste {mention_link}! 🙏\n"
        "Aapka is Telegram Bot par swagat hai. Niche diye gaye button par click karke"
        " commands ki jankari lein:"
    )
    reply_markup = InlineKeyboardMarkup(get_main_menu_keyboard())
    await query.edit_message_text(
        welcome_message, reply_markup=reply_markup, parse_mode="HTML"
    )

  elif query.data == "help_menu":
    help_text = (
        "📖 **ALL COMMANDS & INSTRUCTIONS**:\n\n"
        "1. **/start** - Bot ko start karne aur main menu kholne ke liye.\n"
        "2. **/gensession <API_ID> <API_HASH>** - Bot ke DM mein secure session"
        " string generate karne ke liye.\n"
        "3. **/tagall [message]** - Telegram group ke sabhi active members ko"
        " tag karne ke liye (Sirf Admin)."
    )
    back_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_home")]]
    )
    await query.edit_message_text(
        help_text, reply_markup=back_keyboard, parse_mode="Markdown"
    )

  elif query.data == "gen_session":
    gen_text = (
        "🔑 **GenSession Guide**:\n\n"
        "• Yeh command sirf **Bot ke Personal Chat (DM)** mein kaam karti"
        " hai.\n"
        "• Format: `/gensession <API_ID> <API_HASH>`\n"
        "• Iske baad bot aapse phone number aur OTP maangega."
    )
    back_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_home")]]
    )
    await query.edit_message_text(
        gen_text, reply_markup=back_keyboard, parse_mode="Markdown"
    )

  elif query.data == "tagall_info":
    tagall_text = (
        "🏷️ **Tagall Guide**:\n\n"
        "• Yeh command sirf **Telegram Groups** mein kaam karti hai.\n"
        "• Ise use karne ke liye aapka group mein **Admin** hona zaroori hai.\n"
        "• Format: `/tagall Jaldi sabhi online aa jao!`"
    )
    back_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_home")]]
    )
    await query.edit_message_text(
        tagall_text, reply_markup=back_keyboard, parse_mode="Markdown"
    )


def main():
  TOKEN = os.environ.get("BOT_TOKEN")

  if not TOKEN:
    logger.error("❌ Error: BOT_TOKEN environment variable set nahi hai!")
    return

  application = ApplicationBuilder().token(TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_click_handler))

  setup_tagall(application)
 # setup_session_gen(application) 
    
  logger.info("Bot polling start ho rahi hai...")
  application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 10000))
  flask_thread = threading.Thread(
      target=lambda: app.run(host="0.0.0.0", port=port)
  )
  flask_thread.daemon = True
  flask_thread.start()

  main()
  

