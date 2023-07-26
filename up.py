import asyncio
import os
from pyrogram import Client

# اطلاعات API تلگرام
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

# اطلاعات API پیروگرام
api_id_pyrogram = YOUR_PYROGRAM_API_ID
api_hash_pyrogram = 'YOUR_PYROGRAM_API_HASH'

# تعریف صف برای فایل‌ها
file_queue = asyncio.Queue()

# تابع برای آپلود فایل با Pyrogram
async def upload_file(client, chat_id, file_path):
    try:
        message = await client.send_document(chat_id, file_path)
        print(f"فایل با موفقیت آپلود شد: {file_path}")
        os.remove(file_path)  # پاک‌کردن فایل از سرور پس از آپلود
        file_queue.task_done()
        return message
    except Exception as e:
        print(f"خطا در آپلود فایل {file_path}: {e}")
        file_queue.task_done()

# تابع برای پردازش صف و آپلود فایل‌ها با Pyrogram
async def process_file_queue(client, chat_id):
    async for file_path in file_queue:
        await upload_file(client, chat_id, file_path)

async def main():
    # اجرای Pyrogram
    async with Client("my_account", api_id_pyrogram, api_hash_pyrogram, bot_token=bot_token) as pyrogram_client:
        # استفاده از pyrogram و اضافه کردن فایل‌ها به صف
        # links = ['لینک ۱', 'لینک ۲', ...]
        links = ['link1.txt', 'link2.txt', 'link3.txt']  # یک لیست از لینک‌ها یا نام فایل‌ها
        chat_id = "me"  # chat_id خودتان یا chat_id کاربر/گروه/کانال دیگری که می‌خواهید آپلود شود

        for link in links:
            # اینجا می‌توانید بر اساس لینک فایل‌ها را دانلود کرده و در صف قرار دهید
            await file_queue.put(link)

        # تعریف ۵ تا ورکر برای همزمانی (concurrent) در آپلود فایل‌ها
        num_workers = 5
        tasks = [process_file_queue(pyrogram_client, chat_id) for _ in range(num_workers)]

        # شروع همه ورکر‌ها
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
