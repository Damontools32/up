import os
import requests
from pyrogram import Client

# وارد کردن توکن ربات
API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

# ایجاد ارتباط با ربات
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# تعریف تابع برای دانلود فایل از لینک
def download_file(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

# ارسال لینک‌های دانلود به ربات
async def send_links(links):
    # برای دانلود فایل‌ها به ترتیب زمان دانلود، لینک‌های دانلود را مرتب می‌کنیم
    sorted_links = sorted(links, key=lambda x: x[1])
    for link, _ in sorted_links:
        # دانلود فایل از لینک
        file_name = link.split("/")[-1]
        download_file(link, file_name)
        # آپلود فایل به تلگرام
        await app.send_document("me", file_name)
        # حذف فایل از سیستم
        os.remove(file_name)

# شروع اجرای برنامه
with app:
    # خواندن لینک‌های دانلود از کاربر
    links = []
    async for message in app.iter_messages("me"):
        if message.document:
            links.append((message.text, message.date))
    # ارسال لینک‌های دانلود به ربات
    await send_links(links)
