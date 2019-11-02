import telebot
from telebot.types import Message
from telebot import types
from threading import Thread
import time
import schedule
import datetime

TOKEN = '1052618109:AAGCUts9_VvN97wyx8sKpii07eedU0F4mxw'
bot = telebot.TeleBot(TOKEN)

cities = ['Москва', 'Пермь', 'Челябинск', 'Омск', 'Уфа', 'Ижевск']

# {chat_id: city}
users = dict()

proc = None


def lunch_cleaner():
    now = datetime.datetime.now()
    lunchs = []  # TODO: Заменить на запрос в БД
    for lunch in lunchs:
        splitted = lunch.time.split(':')
        hours = int(splitted[0])
        minutes = int(splitted[1])
        lunch_time = datetime.datetime.now()
        lunch_time.replace(hour=hours, minute=minutes, second=0)
        if (now - lunch_time).total_seconds() // 60 == 15:
            users = []  # TODO: достать user_id всех пользаков, кто зареган в данном обеде(lunch_id)
            for user in users:
                bot.send_message(user.chat.id, "До обеда осталось 15 минут, встреча будет в " + lunch.place)
        if now > lunch_time:
            print('Шедулер типо удоляет обед')
            # TODO: удалить ланч по id (lunch.id)


schedule.every().minute.do()


def shedule_helper():
    while True:
        schedule.run_pending()
        time.sleep(1)


alarmer = Thread(target=shedule_helper, daemon=True)


@bot.message_handler(func=lambda message: message.chat.id not in users)
def kit_start(message):
    select_city(message)


@bot.message_handler(commands=['start'])
def city_change(message):
    select_city(message)


def select_city(message):
    global users
    global cities
    keyboard = types.InlineKeyboardMarkup()
    for city in cities:
        keyboard.add(types.InlineKeyboardButton(city, callback_data='add_city:' + city))
    bot.send_message(message.chat.id, "Выберите свой город",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'add_city' in call.data)
def city_setter(call):
    global users
    city = call.data.split(':')[1]
    users[call.message.chat.id] = city
    bot.send_message(call.message.chat.id,
                     "Вы выбрали город " + city + ", теперь ваши обеды будут проходить именно здесь!")


@bot.message_handler(commands=['help'])
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
    bot.send_message(call.message.chat.id,
                     'Мы учтем ваши пожелания, а теперь выберите время в которое вы бы хотели пообедать')
    # ToDo вбивает время, заявка закончилась


bot.polling()
