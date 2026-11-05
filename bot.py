import logging
import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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


# Simple Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(
      "🎉 Bhai! Bot ne successfully environment variable se response de diya"
      " hai!"
  )


def main():
  # Environment variable se token uthana
  TOKEN = os.environ.get("BOT_TOKEN")

  if not TOKEN:
    logger.error("❌ Error: BOT_TOKEN environment variable set nahi hai!")
    return

  application = ApplicationBuilder().token(TOKEN).build()

  # Start handler add karna
  application.add_handler(CommandHandler("start", start))

  logger.info("Bot polling start ho rahi hai...")

  # Webhook conflicts clear karke polling start karna
  application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
  import threading

  # Flask server ko alag thread mein chalana taaki Render port scan pass kar sake
  port = int(os.environ.get("PORT", 10000))
  flask_thread = threading.Thread(
      target=lambda: app.run(host="0.0.0.0", port=port)
  )
  flask_thread.daemon = True
  flask_thread.start()

  # Bot main function chalana
  main()
    
