# وارد کردن اطلاعات ربات
api_id = 123456 # شماره شناسایی api
api_hash = "abcdef1234567890" # رشته شناسایی api
bot_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" # توکن ربات

# ایجاد یک نمونه از کلاس TelegramClient
from telethon import TelegramClient, events
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# تعریف یک تابع برای دانلود و آپلود فایل اسپاتیفای
def download_and_upload(spotify_link, event):
    # استفاده از Spotdl برای دانلود فایل mp3 از لینک اسپاتیفای
    from spotdl.command_line.core import Spotdl
    args = {
        "no_encode": True,
    }
    with Spotdl(args) as spotdl_handler:
        spotdl_handler.download_track(spotify_link)
    # پیدا کردن نام فایل دانلود شده
    import os
    file_name = os.listdir()[0]
    # آپلود فایل به تلگرام با استفاده از telethon
    bot.send_file(event.chat_id, file_name, caption="Here is your song")
    # حذف فایل از سیستم
    os.remove(file_name)

# تعریف یک رویداد برای دریافت لینک اسپاتیفای از کاربر
@bot.on(events.NewMessage(pattern=r"https://open.spotify.com/track/.*"))
async def spotify_handler(event):
    # گرفتن لینک اسپاتیفای از پیام کاربر
    spotify_link = event.text
    # نمایش یک پیام در حال پردازش به کاربر
    await event.reply("Processing your request...")
    # فراخوانی تابع دانلود و آپلود با لینک و رویداد به عنوان ورودی‌ها
    download_and_upload(spotify_link, event)

# شروع ربات و حفظ آن در حالت فعال
bot.run_until_disconnected()
