from pyrogram import Client, filters
from config import platinum_users, OWNER_ID  # Import from config.py

# /cloneftm command for Platinum users
@Client.on_message(filters.command('cloneftm') & filters.private)
async def clone_bot(client, message):
    user_id = message.from_user.id

    if user_id not in platinum_users:
        await message.reply("❌ You are not a Platinum user. Please contact the owner @ftmdeveloper to subscribe to the Platinum plan.")
        return
    
    await message.reply("✅ You are a Platinum user! Please forward the bot token from BotFather.")

    # Further implementation for processing the bot token will go here
    # bot_token = process_forwarded_message(message)


# /addplatinum command (Owner/admin can use this to add users)
@Client.on_message(filters.command('addplatinum') & filters.user(OWNER_ID))
async def add_platinum(client, message):
    try:
        # Admin or owner adds Platinum user by Telegram user ID
        user_id = int(message.command[1])
        # Add user to platinum_users dictionary
        platinum_users[user_id] = {'plan': 'Platinum'}
        await message.reply(f"✅ User {user_id} has been granted Platinum subscription!")
    except (IndexError, ValueError):
        await message.reply("❌ Please provide a valid user ID. Usage: /addplatinum <user_id>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
