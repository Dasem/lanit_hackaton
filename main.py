import telebot
from telebot.types import Message
TOKEN = '926423911:AAEM8Wg7ycg1oGz8xNzqmNoxLOgU7BXhBBA'
bot = telebot.TeleBot(TOKEN)

proc = None


@bot.message_handler(commands=['r'])
def redeploy(message: Message):
    bot.send_message(message.from_chat, 'soobshenie')


bot.polling()
