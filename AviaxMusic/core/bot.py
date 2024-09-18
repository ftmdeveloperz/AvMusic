import uvloop
uvloop.install()

from pyrogram import Client, errors, filters
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
from platinum_feature import *  # Import the Platinum plan logic
from clone_feature import clone_bot  # Import clone feature from separate file
from ..logging import LOGGER


class Aviax(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="AviaxMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Notify log group about the bot starting
        try:
            await self.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=(
                    f"<u><b>» {self.mention} BOT STARTED :</b></u>\n\n"
                    f"ID: <code>{self.id}</code>\n"
                    f"NAME: {self.name}\n"
                    f"USERNAME: @{self.username}"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason: {type(ex).__name__}."
            )
            exit()

        # Ensure the bot is an admin in the log group
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()

        # Bot started successfully
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()

# Register the commands in the main function
def main():
    bot = Aviax()

    # Add clone bot feature for Platinum users
    bot.add_handler(Client.on_message(filters.command('cloneftm') & filters.private)(clone_bot))

    # Start the bot
    bot.run()

if __name__ == "__main__":
    main()
