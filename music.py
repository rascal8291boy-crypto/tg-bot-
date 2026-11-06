import os
import yt_dlp
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# YouTube se audio URL nikalne ke liye ytdl options
ytdl_format_options = {
    "format": "bestaudio/best",
    "bot_token": os.environ.get("BOT_TOKEN"),
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
}


async def play_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
  chat = update.effective_chat
  user = update.effective_user

  if chat.type == "private":
    await update.message.reply_text(
        "❌ Yeh command sirf **Telegram Groups** ke voice chat mein kaam"
        " karti hai!"
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

    await msg.edit_text(
        f"🎵 Playing **{title}** in Voice Chat...\n(Note: Bot ka userbot/client"
        " active hona zaroori hai)"
    )

    # PyTgCalls ke zariye voice chat mein audio stream karne ka logic
    # (Iske liye Pyrogram client aur PyTgCalls active hone chahiye)

  except Exception as e:
    await msg.edit_text(f"❌ Error: `{str(e)}`")


def setup_music(application):
  application.add_handler(CommandHandler("play", play_music))
  
