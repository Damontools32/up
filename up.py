import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from pyrogram import Client
import aiohttp

# اطلاعات API تلگرام
api_id_telethon = YOUR_TELETHON_API_ID
api_hash_telethon = 'YOUR_TELETHON_API_HASH'
bot_token_telegram = 'YOUR_BOT_TOKEN'

# تابع برای دانلود و آپلود فایل با Pyrogram
async def upload_file_to_telegram(file_path, chat_id):
    async with Client("my_account", bot_token=bot_token_telegram) as app:
        try:
            message = await app.send_document(chat_id, file_path)
            print(f"فایل با موفقیت آپلود شد: {file_path}")
        except Exception as e:
            print(f"خطا در آپلود فایل {file_path}: {e}")

# تابع برای دانلود لینک با استفاده از Telethon
async def download_link(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if response.status == 200:
                filename = link.split("/")[-1]
                with open(filename, "wb") as f:
                    f.write(await response.read())
                return filename
            else:
                return None

# تابع اصلی برای دانلود و آپلود لینک‌ها به ترتیب اولویت زمانی
async def main():
    # لیست لینک‌های دانلود
    download_links = ['link1', 'link2', 'link3']

    # chat_id خودتان یا chat_id کاربر/گروه/کانال دیگری که می‌خواهید آپلود شود
    chat_id = "your_chat_id"

    async with TelegramClient(StringSession(), api_id_telethon, api_hash_telethon) as client:
        for link in download_links:
            filename = await download_link(link)
            if filename:
                await upload_file_to_telegram(filename, chat_id)

if __name__ == "__main__":
    asyncio.run(main())
