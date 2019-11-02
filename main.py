import telebot
from telebot.types import Message
TOKEN = '997103341:AAHEFEGSl6LF4JMxGZus6cMzcQLlhsaHOVQ' # t.me/jrinderBot
bot = telebot.TeleBot(TOKEN)

proc = None


@bot.message_handler(commands=['r'])
def redeploy(message: Message):
    bot.send_message(message.from_chat, 'soobshenie')


bot.polling()
