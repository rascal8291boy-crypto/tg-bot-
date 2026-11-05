import asyncio
from pyrogram import Client
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

# Temporary storage for login states
login_states = {}


async def gensession_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # Sirf DM (Private chat) mein kaam karega
  if update.effective_chat.type != "private":
    await update.message.reply_text(
        "❌ Yeh command sirf bot ke Personal Chat (DM) mein kaam karegi!"
    )
    return

  args = context.args
  if len(args) < 2:
    await update.message.reply_text(
        "❌ **Sahi tareeqa:** `/gensession <API_ID> <API_HASH>`\n\nExample:"
        " `/gensession 1234567 abcdef123456...`"
    )
    return

  try:
    api_id = int(args[0])
    api_hash = args[1]
  except ValueError:
    await update.message.reply_text("❌ API_ID hamesha ek number honi chahiye!")
    return

  user_id = update.effective_user.id

  # --- Event Loop Fix for Pyrogram ---
  try:
    asyncio.get_running_loop()
  except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
  # -----------------------------------

  # Pyrogram client initialize karna session ke liye
  temp_client = Client(
      f"session_gen_{user_id}",
      api_id=api_id,
      api_hash=api_hash,
      in_memory=True,
  )

  try:
    await temp_client.connect()
  except Exception as e:
    await update.message.reply_text(f"❌ Connection Error: `{str(e)}`")
    return

  login_states[user_id] = {"client": temp_client, "step": "awaiting_phone"}

  await update.message.reply_text(
      "📱 **Session Generator Start Ho Chuka Hai!**\n\nKripya apna Telegram"
      " phone number country code ke sath bhejein\n(Jaise: `+919876543210`):"
  )


async def handle_session_steps(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
  if update.effective_chat.type != "private":
    return

  user_id = update.effective_user.id
  if user_id not in login_states:
    return

  state = login_states[user_id]
  temp_client = state["client"]
  step = state["step"]
  text = update.message.text.strip()

  if step == "awaiting_phone":
    state["phone"] = text
    try:
      sent_code = await temp_client.send_code(text)
      state["phone_code_hash"] = sent_code.phone_code_hash
      state["step"] = "awaiting_otp"
      await update.message.reply_text(
          "📩 **OTP Bhej Diya Gaya Hai!**\n\nKripya apne Telegram app par aaya hua"
          " OTP code yahan bhejein \n(Jaise: `12345`):"
      )
    except Exception as e:
      await update.message.reply_text(
          f"❌ Error: `{str(e)}`\nSession generation cancel ho gaya. Dobara"
          " `/gensession` try karein."
      )
      await temp_client.disconnect()
      del login_states[user_id]

  elif step == "awaiting_otp":
    try:
      await temp_client.sign_in(state["phone"], state["phone_code_hash"], text)
      session_string = await temp_client.export_session_string()
      await update.message.reply_text(
          "✅ **Session String Successfully Generate Ho Gayi Hai!**\n\n"
          f"`{session_string}`\n\n⚠️ Ise copy karke safe jagah rakh lein."
      )
      await temp_client.disconnect()
      del login_states[user_id]
    except Exception as e:
      if "SessionPasswordNeeded" in str(e):
        state["step"] = "awaiting_password"
        await update.message.reply_text(
            "🔒 **2-Step Verification Detected!**\n\nKripya apna cloud password"
            " yahan bhejein:"
        )
      else:
        await update.message.reply_text(
            f"❌ Error: `{str(e)}`\nDobara `/gensession` try karein."
        )
        await temp_client.disconnect()
        del login_states[user_id]

  elif step == "awaiting_password":
    try:
      await temp_client.check_password(text)
      session_string = await temp_client.export_session_string()
      await update.message.reply_text(
          "✅ **Session String Successfully Generate Ho Gayi Hai!**\n\n"
          f"`{session_string}`\n\n⚠️ Ise copy karke safe jagah rakh lein."
      )
      await temp_client.disconnect()
      del login_states[user_id]
    except Exception as e:
      await update.message.reply_text(
          f"❌ Galat password ya error: `{str(e)}`\nDobara `/gensession` try"
          " karein."
      )
      await temp_client.disconnect()
      del login_states[user_id]


def setup_session_gen(application):
  application.add_handler(CommandHandler("gensession", gensession_start))
  application.add_handler(
      MessageHandler(
          filters.TEXT & (~filters.COMMAND) & filters.PRIVATE,
          handle_session_steps,
      )
    )
          
