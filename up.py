import asyncio
import requests
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# اطلاعات مربوط به ربات تلگرام
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# تعیین تعداد همزمان برای دانلود فایل‌ها
CONCURRENT_DOWNLOADS = 2

async def main():
    # اتصال به تلگرام با کلاینت
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    # شناسه عددی کاربر مجاز برای آپلود فایل‌ها (قرار دادن user_id در اینجا)
    recipient_entity = USER_ID

    # لیست لینک‌های دانلودی
    download_links = [
        'https://example.com/file1.txt',
        'https://example.com/file2.txt',
        'https://example.com/file3.txt'
        # و غیره
    ]

    # اجرای همزمان فرآیند دانلود و آپلود
    tasks = []
    for link in download_links:
        task = download_and_upload(client, link, recipient_entity)
        tasks.append(task)
        if len(tasks) >= CONCURRENT_DOWNLOADS:
            await asyncio.gather(*tasks)
            tasks = []

    # مطمئن شوید که تمام وظایف اجرا شوند
    if tasks:
        await asyncio.gather(*tasks)

    # قطع ارتباط با تلگرام
    await client.disconnect()

async def download_and_upload(client, link, recipient_entity):
    # دانلود فایل از لینک
    file_name = link.split('/')[-1]
    with requests.get(link, stream=True) as response:
        with open(file_name, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)

    # آپلود فایل به تلگرام
    await client.send_file(recipient_entity, file_name)

    # حذف فایل از سرور محلی
    import os
    os.remove(file_name)

if __name__ == '__main__':
    # جایگزین کردن user_id با مقدار مربوطه
    USER_ID = 123456789  # شناسه عددی کاربر مجاز
    asyncio.run(main())
