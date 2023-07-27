import os
import requests
from collections import deque
from telethon import TelegramClient, events
from pyrogram import Client, filters

# setup your credentials
api_id = 'your_api_id'
api_hash = 'your_api_hash'
bot_token = 'your_bot_token'

# setup telegram client
client = TelegramClient('bot', api_id, api_hash)

queue = deque()  # initialize a queue

@client.on(events.NewMessage)
async def message_handler(event):
    if event.message.message.startswith('http'):
        queue.append(event.message.message)

# downloading the file
async def download_file():
    while len(queue) > 0:
        url = queue.popleft()  # pop the first URL from the queue
        r = requests.get(url, stream=True)
        
        filename = url.split("/")[-1]
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: 
                    f.write(chunk)

# uploading the file
app = Client("my_account", api_id, api_hash, bot_token = bot_token)

@app.on_message()
async def upload_file(client, message):
    filename = message.text
    await app.send_document("me", document=filename)

# start download and upload task
download_file()
upload_file()

client.start()
client.run_until_disconnected()
