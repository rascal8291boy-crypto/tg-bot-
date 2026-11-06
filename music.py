import os
import yt_dlp
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Userbot client (Session string ke zariye voice chat join karega)
# Iske liye environment variable me STRING_SESSION set karna hoga
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "")

userbot = None
pytg = None

if STRING_SESSION and API_ID and API_HASH:
  try:
    userbot = Client(
        "music_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
        in_memory=True,
    )
    pytg = PyTgCalls(userbot)
  except Exception as e:
    print(f"Userbot init error: {e}")

ytdl_format_options = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
}


async def play_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
  chat = update.effective_chat

  if chat.type == "private":
    await update.message.reply_text(
        "❌ Yeh command sirf **Telegram Groups** ke voice chat mein kaam karti"
        " hai!"
    )
    return

  if not userbot or not pytg:
    await update.message.reply_text(
        "❌ Userbot configure nahi hai! Environment variables (API_ID,"
        " API_HASH, STRING_SESSION) check karein."
    )
    return

  if not context.args:
    await update.message.reply_text(
        "❌ Kripya gaane ka naam likhein!\nExample: `/play Kesariya`"
    )
    return

  query = " ".join(context.args)
  msg = await update.message.reply_text(
      f"🔎 Searching for `{query}` on YouTube..."
  )

  try:
    with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
      info = ydl.extract_info(f"ytsearch:{query}", download=False)
      if "entries" in info:
        info = info["entries"][0]

      url = info["url"]
      title = info["title"]

    # Userbot ko voice chat mein start karna
    if not userbot.is_connected:
      await userbot.start()
    if not pytg.is_connected:
      await pytg.start()

    await pytg.join_group_call(chat.id, AudioPiped(url))

    await msg.edit_text(
        f"🎵 Now Playing in Voice Chat:\n**{title}** 🎶\nRequested by:"
        f" {update.effective_user.first_name}"
    )

  except Exception as e:
    await msg.edit_text(f"❌ Error: `{str(e)}`")


async def stop_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
  chat = update.effective_chat
  if chat.type == "private":
    return

  try:
    if pytg and pytg.is_connected:
      await pytg.leave_group_call(chat.id)
      await update.message.reply_text(
          "⏹️ Music stopped and voice chat left successfully!"
      )
    else:
      await update.message.reply_text("❌ Voice chat connected nahi hai!")
  except Exception as e:
    await update.message.reply_text(f"❌ Error: `{str(e)}`")


def setup_music(application):
  application.add_handler(CommandHandler("play", play_music))
  application.add_handler(CommandHandler("stop", stop_music))
        
