import config
from pyrogram import filters

# Define clone bot feature for Platinum users
async def clone_bot(client, message):
    user_id = message.from_user.id

    # Check if the user is a Platinum subscriber
    if user_id not in config.platinum_users:
        await message.reply("❌ You are not a Platinum user. Please contact the owner @ftmdeveloper to subscribe to the Platinum plan.")
        return

    await message.reply("✅ You are a Platinum user! Please forward the bot token from BotFather.")

    # Check for forwarded message with bot token from BotFather
    @client.on_message(filters.forwarded & filters.private)
    async def process_forwarded_token(client, forwarded_message):
        try:
            # Assuming the forwarded message contains the token
            bot_token = forwarded_message.text.strip()
            if len(bot_token) == 45:  # Bot tokens are 45 characters long
                await message.reply(f"✅ Bot token received: <code>{bot_token}</code>\nPlease wait while we set up your bot.")
                # Here you can add logic to deploy a cloned bot using the bot token
                # Example logic could be connecting to a bot cloning service
            else:
                await message.reply("❌ Invalid bot token. Please forward a valid token from BotFather.")
        except Exception as e:
            await message.reply(f"❌ Error processing the token: {str(e)}")
