import telebot
import re

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(func=lambda message: True)
def handle_message(message):

  if message.text.startswith("https://drive.google.com"):
    
    file_id = re.search(r"/d/([^/]*)", message.text).group(1)

    download_link = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key=AIzaSyBKNu2mYKZgnm5TsIhGOCeCYg6eRHOosJ0"
    
    bot.send_message(message.chat.id, download_link)

bot.polling()
