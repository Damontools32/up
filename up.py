import telethon
import pyrogram

# Get the API ID, API hash, and bot token from your Telegram bot settings
API_ID = 1234567890
API_HASH = "abcdeghijklmnopqrstuvwxyz1234567890"
BOT_TOKEN = "1234567890:abcdeghijklmnopqrstuvwxyz1234567890"

# Create a Telethon client
client = telethon.TelegramClient("bot", API_ID, API_HASH)

# Connect the client to Telegram
client.connect()

# Get the list of messages sent to the bot
messages = client.get_messages()

# Loop over the messages
for message in messages:
    # If the message is a link
    if message.text.startswith("https://") or message.text.startswith("http://"):
        # Download the file
        file = client.download_file(message.text)

        # Upload the file to Telegram
        pyrogram.send_file(
            chat_id=message.chat_id,
            file=file,
            caption="This is the file you sent.",
        )

        # Delete the file from the server
        client.delete_file(file)

# Disconnect the client from Telegram
client.disconnect()
