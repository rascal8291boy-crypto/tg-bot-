from flask import Flask
import logging
import os
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Tagall wale module ko import karna
from session_gen import setup_session_gen
from tagall import setup_tagall

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Render ke liye Flask server
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is alive and running!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# /start command handler (Inline Buttons ke sath)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user
  mention_link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'

  welcome_message = (
      f"Namaste {mention_link}! 🙏\n"
      "Aapka is Telegram Bot par swagat hai. Kripya niche diye gaye buttons mein se"
      " kisi par click karke instructions dekhein:"
  )

  # Buttons layout
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


# Button click handler (Instructions dikhane ke liye)
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()  # Loading animation hatane ke liye

  if query.data == "help_menu":
    help_text = (
        "📖 **ALL COMMANDS & INSTRUCTIONS**:\n\n"
        "1. **/start** - Bot ko start karne aur main menu dekhne ke liye.\n"
        "2. **/gensession <API_ID> <API_HASH>** - Bot ke DM mein secure session"
        " string generate karne ke liye.\n"
        "3. **/tagall [message]** - Telegram group ke sabhi active members ko"
        " tag karne ke liye (Sirf Admin).\n\n"
        "Kisi aur button par click karke specific jankari le sakte hain!"
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


if __name__ == "__main__":
  # Flask server background thread mein chalana
  t = threading.Thread(target=run_flask)
  t.start()

  # Apna Bot Token yahan dalein
  TOKEN = os.environ.get("BOT_TOKEN")
    
  application = ApplicationBuilder().token(TOKEN).build()

  # /start handler aur Button click handler add karna
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_click_handler))

  # Module handlers add karna
  setup_tagall(application)
  setup_session_gen(application)

  print("Bot aur Web Server successfully start ho chuke hain...")
  application.run_polling()
