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


# /start command with Inline Buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user
  mention_link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'

  welcome_message = (
      f"Namaste {mention_link}! 🙏\n"
      "Aapka is Telegram Bot par swagat hai. Niche diye gaye button par click karke"
      " commands ki jankari lein:"
  )

  # Interactive buttons layout
  keyboard = [
      [InlineKeyboardButton("💡 HELP & COMMANDS", callback_data="help_menu")],
      [
          InlineKeyboardButton("🔑 GEN SESSION", callback_data="gen_session"),
          InlineKeyboardButton("🏷️ TAGALL INFO", callback_data="tagall_info"),
      ],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await update.message.reply_text(
      welcome_message, reply_markup=reply_markup, parse_mode="HTML"
  )


# Button click handler for instructions
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()  # Loading effect hatane ke liye

  if query.data == "help_menu":
    help_text = (
        "📖 **ALL COMMANDS & INSTRUCTIONS**:\n\n"
        "1. **/start** - Bot ko start karne aur main menu kholne ke liye.\n"
        "2. **/gensession <API_ID> <API_HASH>** - Bot ke DM mein secure session"
        " string generate karne ke liye.\n"
        "3. **/tagall [message]** - Telegram group ke sabhi active members ko"
        " tag karne ke liye (Sirf Admin).\n\n"
        "Kisi bhi specific feature ki jankari ke liye niche wale buttons use"
        " karein!"
    )
    await query.edit_message_text(help_text, parse_mode="Markdown")

  elif query.data == "gen_session":
    gen_text = (
        "🔑 **GenSession Guide**:\n\n"
        "• Yeh command sirf **Bot ke Personal Chat (DM)** mein kaam karti"
        " hai.\n"
        "• Format: `/gensession <API_ID> <API_HASH>`\n"
        "• Iske baad bot aapse phone number aur OTP maangega."
    )
    await query.edit_message_text(gen_text, parse_mode="Markdown")

  elif query.data == "tagall_info":
    tagall_text = (
        "🏷️ **Tagall Guide**:\n\n"
        "• Yeh command sirf **Telegram Groups** mein kaam karti hai.\n"
        "• Ise use karne ke liye aapka group mein **Admin** hona zaroori hai.\n"
        "• Format: `/tagall Jaldi sabhi online aa jao!`"
    )
    await query.edit_message_text(tagall_text, parse_mode="Markdown")


def main():
  # Environment variable se token uthana
  TOKEN = os.environ.get("BOT_TOKEN")

  if not TOKEN:
    logger.error("❌ Error: BOT_TOKEN environment variable set nahi hai!")
    return

  application = ApplicationBuilder().token(TOKEN).build()

  # Handlers add karna
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_click_handler))

  logger.info("Bot polling start ho rahi hai...")

  # Webhook conflicts clear karke polling start karna
  application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
  # Flask server ko alag thread mein chalana taaki Render port scan pass kar sake
  port = int(os.environ.get("PORT", 10000))
  flask_thread = threading.Thread(
      target=lambda: app.run(host="0.0.0.0", port=port)
  )
  flask_thread.daemon = True
  flask_thread.start()

  # Bot main function chalana
  main()
        
