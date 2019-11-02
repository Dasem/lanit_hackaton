import telebot
from telebot.types import Message
from telebot import types

TOKEN = '1052618109:AAGCUts9_VvN97wyx8sKpii07eedU0F4mxw'
bot = telebot.TeleBot(TOKEN)

proc = None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     "Приветствую " + name + ", я бот для поиска компании для обедов. Если хочешь найти себе компанию, чтобы вместе вкусно поесть, ты попал по адресу.Всё что нужно это написать мне /dinner")


@bot.message_handler(commands=['dinner'])
def handle_text(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Присоединиться', callback_data='join'),
                 types.InlineKeyboardButton('Предложить', callback_data='add'))
    bot.send_message(message.chat.id, "Вы хотите присоединиться к кому-то на обед или оставить свое предложение?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'join':
        bot.send_message(call.message.chat.id, 'Выберите одно из предложениц на обед')
    if call.data == 'add':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Обед с собой', callback_data='stay'),
                     types.InlineKeyboardButton('Пойти на обед', callback_data='go'))
        bot.send_message(call.message.chat.id, "У вас обед с собой или вы хотели бы пойти куда-нибудь?",
                         reply_markup=keyboard)
    if call.data == 'stay':
        bot.send_message(call.message.chat.id, 'Выберите время в которое вы бы хотели пообедать')
        # вбивает время, заявка закончилась будем искать тех кто тоже взял с собой
    if call.data == 'go':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Столовая(первое, второе)', callback_data='rest'),
                     types.InlineKeyboardButton('Кафе, фастфуд', callback_data='cafe'))
        bot.send_message(call.message.chat.id, "Куда бы вы хотели пойти?",
                         reply_markup=keyboard)
    if call.data == 'rest':
        bot.send_message(call.message.chat.id, 'Выберите время в которое вы бы хотели пообедать')
        # вбивает время, заявка закончилась будем искать тех кто тоже хочет в столовую
    if call.data == 'cafe':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Пицца', callback_data='rest'),
                     types.InlineKeyboardButton('Суши', callback_data='cafe'),
                     types.InlineKeyboardButton('Суши', callback_data='cafe'),
                     types.InlineKeyboardButton('Суши', callback_data='cafe'),
                     types.InlineKeyboardButton('Суши', callback_data='cafe'),
                     types.InlineKeyboardButton('Суши', callback_data='cafe'),
                     types.InlineKeyboardButton('Суши', callback_data='cafe'),
                     types.InlineKeyboardButton('Суши', callback_data='cafe'))
        bot.send_message(call.message.chat.id, "Какие у вас предпочтения?",
                         reply_markup=keyboard)

bot.polling()
