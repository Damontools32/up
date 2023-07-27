# نصب کتابخانه‌های مورد نیاز
pip install telethon
pip install spotdl

# وارد کردن اطلاعات ربات
api_id = 123456 # شماره شناسایی api
api_hash = "abcdef1234567890" # رشته شناسایی api
bot_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" # توکن ربات

# ایجاد یک نمونه از کلاس TelegramClient
from telethon import TelegramClient, events
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# تعریف یک تابع برای دانلود و آپلود فایل اسپاتیفای
def download_and_upload(spotify_link, event):
    # استفاده از spotdl برای دانلود فایل mp3 از لینک اسپاتیفای
    import spotdl
    spotdl.download_track(spotify_link)
    # پیدا کردن نام فایل دانلود شده
    import os
    file_name = os.listdir()[0]
    # آپلود فایل به تلگرام با استفاده از telethon
    bot.send_file(event.chat_id, file_name)
    # حذف فایل از سرور
    os.remove(file_name)

# تعریف یک رویداد برای دریافت پیام‌های حاوی لینک اسپاتیفای
@bot.on(events.NewMessage(pattern="https://open.spotify.com/.*"))
async def spotify_handler(event):
    # گرفتن لینک اسپاتیفای از پیام
    spotify_link = event.text
    # فرستادن یک پاسخ به کاربر برای نشان دادن وضعیت دانلود
    await event.reply("در حال دانلود فایل ...")
    # صدا زدن تابع دانلود و آپلود با لینک و رویداد به عنوان ورودی‌ها
    download_and_upload(spotify_link, event)

# شروع حلقه رویداد‌ها برای گوش دادن به پیام‌ها
bot.run_until_disconnected()
