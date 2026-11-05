from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

# User login states ko track karne ke liye temporary dictionary
login_states = {}

def setup_session_generator(app: Client):
    
    # Step 1: Command se API ID aur API Hash lena
    @app.on_message(filters.command("gensession") & filters.private)
    async def start_gensession(client, message):
        args = message.command
        if len(args) < 3:
            await message.reply_text(
                "❌ **Sahi tareeqa:** `/gensession <API_ID> <API_HASH>`\n\n"
                "Example: `/gensession 1234567 abcdef123456...`"
            )
            return
        
        try:
            api_id = int(args[1])
            api_hash = args[2]
        except ValueError:
            await message.reply_text("❌ API_ID hamesha ek number honi chahiye!")
            return

        chat_id = message.chat.id
        
        # Is user ke liye ek temporary Pyrogram client banana
        temp_client = Client(
            f"session_gen_{chat_id}",
            api_id=api_id,
            api_hash=api_hash,
            in_memory=True
        )
        
        try:
            await temp_client.connect()
        except Exception as e:
            await message.reply_text(f"❌ Connection Error: `{str(e)}`")
            return
        
        # State save karna
        login_states[chat_id] = {
            "client": temp_client,
            "step": "awaiting_phone",
            "api_id": api_id,
            "api_hash": api_hash
        }
        
        await message.reply_text(
            "📱 **Session Generator Start Ho Chuka Hai!**\n\n"
            "Kripya apna Telegram phone number country code ke sath bhejein\n(Jaise: `+919876543210`):"
        )

    # Step 2: Chat mein aane wale inputs (Phone, OTP, Password) ko handle karna
    @app.on_message(filters.private & ~filters.command)
    async def handle_login_steps(client, message):
        chat_id = message.chat.id
        if chat_id not in login_states:
            return
        
        state = login_states[chat_id]
        temp_client = state["client"]
        step = state["step"]
        text = message.text.strip()

        # Phone Number Handle Karna
        if step == "awaiting_phone":
            phone = text
            state["phone"] = phone
            try:
                sent_code = await temp_client.send_code(phone)
                state["phone_code_hash"] = sent_code.phone_code_hash
                state["step"] = "awaiting_otp"
                await message.reply_text(
                    "📩 **OTP Bhej Diya Gaya Hai!**\n\n"
                    "Kripya apne Telegram app par aaya hua OTP code yahan bhejein "
                    "(Agar numbers ke beech space ho toh bina space ke likhein, jaise `1 2 3 4 5` ki jagah `12345`):"
                )
            except Exception as e:
                await message.reply_text(f"❌ Error: `{str(e)}`\nSession generation cancel ho gaya. Dobara `/gensession` try karein.")
                await temp_client.disconnect()
                del login_states[chat_id]

        # OTP Handle Karna
        elif step == "awaiting_otp":
            otp = text
            phone = state["phone"]
            phone_code_hash = state["phone_code_hash"]
            try:
                await temp_client.sign_in(phone, phone_code_hash, otp)
                session_string = await temp_client.export_session_string()
                
                await message.reply_text(
                    f"✅ **Session String Successfully Generate Ho Gayi Hai!**\n\n"
                    f"`{session_string}`\n\n"
                    "⚠️ Ise copy karke safe jagah rakh lein. Yeh aapke bot ke liye secure hai!"
                )
                await temp_client.disconnect()
                del login_states[chat_id]
                
            except SessionPasswordNeeded:
                state["step"] = "awaiting_password"
                await message.reply_text(
                    "🔒 **2-Step Verification Detected!**\n\n"
                    "Aapke account par cloud password laga hai. Kripya apna password yahan bhejein:"
                )
            except (PhoneCodeInvalid, PhoneCodeExpired) as e:
                await message.reply_text(f"❌ Galat ya Expired OTP: `{str(e)}`\nKripya `/gensession` se dobara shuru karein.")
                await temp_client.disconnect()
                del login_states[chat_id]
            except Exception as e:
                await message.reply_text(f"❌ Error: `{str(e)}`")
                await temp_client.disconnect()
                del login_states[chat_id]

        # 2FA Password Handle Karna
        elif step == "awaiting_password":
            password = text
            try:
                await temp_client.check_password(password)
                session_string = await temp_client.export_session_string()
                
                await message.reply_text(
                    f"✅ **Session String Successfully Generate Ho Gayi Hai!**\n\n"
                    f"`{session_string}`\n\n"
                    "⚠️ Ise copy karke safe jagah rakh lein."
                )
                await temp_client.disconnect()
                del login_states[chat_id]
                
            except Exception as e:
                await message.reply_text(f"❌ Galat password ya error: `{str(e)}`\nDobara `/gensession` se try karein.")
                await temp_client.disconnect()
                del login_states[chat_id]
