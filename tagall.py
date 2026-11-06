from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Group ke users ko store karne ke liye dictionary: {chat_id: {user_id: user_name}}
group_users = {}


# Group mein aane wale messages se users ko track karne ka function
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.effective_chat and update.effective_user:
    chat_id = update.effective_chat.id
    user = update.effective_user

    # Sirf groups ya supergroups ke liye aur bot ke messages ignore karne ke liye
    if update.effective_chat.type in ["group", "supergroup"]:
      if not user.is_bot:
        if chat_id not in group_users:
          group_users[chat_id] = {}
        # User ki ID aur Name save karlo
        group_users[chat_id][user.id] = user.first_name


# /tagall command handler function (Sirf Admins ke liye)
async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
  chat = update.effective_chat
  user = update.effective_user

  if chat.type not in ["group", "supergroup"]:
    await update.message.reply_text("❌ Yeh command sirf groups mein use hoti hai!")
    return

  # --- Yahan Admin Check Ho Raha Hai ---
  try:
    member = await chat.get_member(user.id)
    # Agar user admin ya creator nahi hai, toh rok do
    if member.status not in ["administrator", "creator"]:
      await update.message.reply_text(
          "❌ Yeh command sirf group ke admins ke liye hai!"
      )
      return
  except Exception as e:
    print(f"Admin check error: {e}")
    await update.message.reply_text("❌ Admin status check karne mein error aaya.")
    return
  # -------------------------------------

  chat_id = chat.id

  if chat_id not in group_users or not group_users[chat_id]:
    await update.message.reply_text(
        "⚠️ Koi active user track nahi hua hai! Pehle kuch messages aane dein."
    )
    return

  custom_message = (
      " ".join(context.args) if context.args else "Jaldi sabhi online aa jao! 🚨"
  )

  mentions = []
  for user_id, user_name in group_users[chat_id].items():
    mentions.append(f'<a href="tg://user?id={user_id}">{user_name}</a>')

  tags_text = " ".join(mentions)
  final_text = f"<b>{custom_message}</b>\n\n{tags_text}"

  # Telegram message length limit handle karne ke liye
  if len(final_text) > 4000:
    final_text = final_text[:4000]

  await update.message.reply_text(final_text, parse_mode="HTML")


# Is function ko call karke main bot mein handlers add kar denge
def setup_tagall(application):
  application.add_handler(CommandHandler("tagall", tagall))
  application.add_handler(
      MessageHandler(filters.TEXT & (~filters.COMMAND), track_users)
    )
    
