import telebot
from telebot.types import Message
from telebot import types
import dao
import userService

TOKEN = '997103341:AAHEFEGSl6LF4JMxGZus6cMzcQLlhsaHOVQ'  # t.me/jrinderBot
bot = telebot.TeleBot(TOKEN)

cities = ['Москва', 'Пермь', 'Челябинск', 'Омск', 'Уфа', 'Ижевск']

# {chat_id: city}
users = dict()

proc = None


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
    userService.add(int(3), "city", int(-1))
    s = []
    s.append("Вы выбрали город ")
    s.append(city)
    s.append(", теперь ваши обеды будут проходить именно здесь!")

    userService.findById(int(3))
    bot.send_message(call.message.chat.id)

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


def main():
    dao.initDbTables()
    bot.polling()


if __name__ == '__main__':
    main()
