import os
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from dotenv import load_dotenv

load_dotenv()

API_ID = os.environ.get("API_ID")     # Get it from my.telegram.org
API_HASH = os.environ.get("API_HASH") # Get it from my.telegram.org
BOT_TOKEN = os.environ.get("BOT_TOKEN") # Get it from @BotFather

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# This filter will capture all messages containing a link
@app.on_message(filters.regex(r'\b(?:https?://)?(?:www\.)?instagram\.com/p/[-a-zA-Z0-9()@:%_\+.~#?&//=]*\b'))
def handle_instagram_reels(client, message):
    url = message.text
    filename = download_from_instagram(url)
    send_to_telegram(filename)

def download_from_instagram(url):
    options = {
        'format': 'best[ext=mp4]',  # choose the best quality format
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # name the file the URL_ID.mp4
    }
    with YoutubeDL(options) as ydl:
        r = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(r)
    return filename

def send_to_telegram(filename):
    app.send_video(chat_id, filename)

app.run()

