# Import the telethon library
from telethon import TelegramClient, events

# Define the api id, api hash and bot token of your bot
api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

# Create a TelegramClient object with your bot credentials
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Define a function to download instagram posts, reels and stories from a link
def download_instagram(link):
    # You can use an online service or write your own script here
    # For example, using https://downloadgram.com/
    import requests
    from bs4 import BeautifulSoup
    # Send a request to the service with the link as a parameter
    response = requests.get("https://downloadgram.com/", params={"url": link})
    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the download button element in the HTML
    download_button = soup.find("a", class_="btn btn-primary")
    # Get the download link from the href attribute of the button
    download_link = download_button["href"]
    # Download the file from the link and save it locally
    file_name = link.split("/")[-2] + ".mp4" # You can change the file name and extension as you wish
    file_content = requests.get(download_link).content
    with open(file_name, "wb") as f:
        f.write(file_content)
    # Return the file name
    return file_name

# Register an event handler for messages that start with /download
@bot.on(events.NewMessage(pattern="/download"))
async def download_handler(event):
    # Get the message text and sender id
    message = event.message.text
    sender_id = event.message.sender_id
    # Split the message by space and get the second part as the link
    link = message.split()[1]
    # Call the download_instagram function with the link and get the file name
    file_name = download_instagram(link)
    # Send the file to the sender as a document
    await bot.send_file(sender_id, file_name, caption="Here is your file")
    # Delete the file from the local storage
    import os
    os.remove(file_name)

# Start the bot and run it until it is stopped
bot.run_until_disconnected()
