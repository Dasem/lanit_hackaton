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
                     "Приветствую " + name + ", я бот для поиска компании для обедов. Если хочешь найти себе компанию, чтобы вместе вкусно поесть, ты попал по адресу.Всё что нужно это написать мне /lunch")


@bot.message_handler(commands=['lunch'])
def handle_text(message):
    keyboard = types.InlineKeyboardMarkup()
    # ToDo запрос города и личной инфы
    keyboard.add(types.InlineKeyboardButton('Присоединиться', callback_data='join'),
                 types.InlineKeyboardButton('Предложить', callback_data='add'))
    bot.send_message(message.chat.id, "Вы хотите присоединиться к кому-то на обед или оставить свое предложение?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'join')
def query_handler(call):
    bot.send_message(call.message.chat.id, 'Выберите одно из предложениц на обед')


@bot.callback_query_handler(func=lambda call: call.data == 'add')
def query_handler(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Обед с собой', callback_data='stay'),
                 types.InlineKeyboardButton('Пойти на обед', callback_data='go'))
    bot.send_message(call.message.chat.id, "У вас обед с собой или вы хотели бы пойти куда-нибудь?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'stay')
def query_handler(call):
    bot.send_message(call.message.chat.id, 'Выберите время в которое вы бы хотели пообедать')
    # ToDo вбивает время, заявка закончилась будем искать тех кто тоже взял с собой


@bot.callback_query_handler(func=lambda call: call.data == 'go')
def query_handler(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Столовая(первое, второе)', callback_data='rest'),
                 types.InlineKeyboardButton('Кафе, фастфуд', callback_data='cafe'))
    bot.send_message(call.message.chat.id, "Куда бы вы хотели пойти?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'rest')
def query_handler(call):
    bot.send_message(call.message.chat.id, 'Выберите время в которое вы бы хотели пообедать')
    # ToDo вбивает время, заявка закончилась будем искать тех кто тоже хочет в столовую


@bot.callback_query_handler(func=lambda call: call.data == 'cafe')
def query_handler(call):
    keyboard = types.InlineKeyboardMarkup()
    # ToDo брать предпочтения по базе
    keyboard.add(types.InlineKeyboardButton('Пицца', callback_data='pref'),
                 types.InlineKeyboardButton('Суши', callback_data='pref'),
                 types.InlineKeyboardButton('Суши', callback_data='pref'),
                 types.InlineKeyboardButton('Суши', callback_data='pref'),
                 types.InlineKeyboardButton('Суши', callback_data='pref'),
                 types.InlineKeyboardButton('Суши', callback_data='pref'),
                 types.InlineKeyboardButton('Суши', callback_data='pref'),
                 types.InlineKeyboardButton('Суши', callback_data='pref'))
    bot.send_message(call.message.chat.id, "Какие у вас предпочтения?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'pref')
def query_handler(call):
    bot.send_message(call.message.chat.id, 'Мы учтем ваши пожелания, а теперь выберите время в которое вы бы хотели пообедать')
    # ToDo вбивает время, заявка закончилась


bot.polling()
