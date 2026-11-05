import logging
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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


# Simple Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(
      "🎉 Bhai! Bot ne successfully environment variable se response de diya"
      " hai!"
  )


if __name__ == "__main__":
  # Flask server background thread mein chalana
  t = threading.Thread(target=run_flask)
  t.start()

  # Environment variable se token uthana
  TOKEN = os.environ.get("BOT_TOKEN")

  if not TOKEN:
    print(
        "❌ Error: BOT_TOKEN environment variable set nahi hai Render par!"
    )
    exit(1)

  application = ApplicationBuilder().token(TOKEN).build()

  # Start handler add karna
  application.add_handler(CommandHandler("start", start))

  print("Bot polling start ho rahi है...")
  application.run_polling(drop_pending_updates=True)
