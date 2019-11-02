import telebot
from telebot.types import Message
from telebot import types

TOKEN = '1052618109:AAGCUts9_VvN97wyx8sKpii07eedU0F4mxw'
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
    bot.send_message(call.message.chat.id,
                     "Вы выбрали город " + city + ", теперь ваши обеды будут проходить именно здесь!")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     "Приветствую " + name + ", я бот для поиска компании для обедов. Если хочешь найти себе компанию, чтобы вместе вкусно поесть, ты попал по адресу.Всё что нужно это написать мне /lunch")


@bot.message_handler(commands=['lunch'])
def lunch_start(message):
    keyboard = types.InlineKeyboardMarkup()
    # ToDo запрос города и личной инфы
    keyboard.add(types.InlineKeyboardButton('Присоединиться', callback_data='join'),
                 types.InlineKeyboardButton('Предложить', callback_data='create'))
    bot.send_message(message.chat.id, "Вы хотите присоединиться к кому-то на обед или оставить свое предложение?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'join')
def join_handler(call):
    bot.send_message(call.message.chat.id, 'Выберите одно из предложений на обед')


@bot.callback_query_handler(func=lambda call: call.data == 'create')
def create_handler(call):
    msgTime = bot.send_message(call.message.chat.id, 'Введите время для обеда')
    bot.register_next_step_handler(msgTime, set_time)


def set_time(message):
    # ToDo проверить время
    cid = message.chat.id
    meetTime = message.text
    if len(meetTime) == 5:
        ch = [char for char in meetTime]
        hour = ch[0] + ch[1]
        min = ch[3] + ch[4]
        if hour > '24' or hour < '0' or min > '59' or min < '0' or ch[2] != ':':
            msgTime = bot.send_message(message.chat.id, 'Введите корректное время')
            bot.register_next_step_handler(msgTime, set_time)
        else:
            # ToDo добавить время в БД
            msgPlace = bot.send_message(cid, 'Введите место встречи')
            bot.register_next_step_handler(msgPlace, set_place, meetTime)

    else:
        msgTime = bot.send_message(message.chat.id, 'Введите корректное время')
        bot.register_next_step_handler(msgTime, set_time)


def set_place(message, meetTime):
    cid = message.chat.id
    meetPlace = message.text
    # ToDo добавить место в БД
    msgGoal = bot.send_message(cid, 'Введите место для обеда')
    bot.register_next_step_handler(msgGoal, set_goal, meetTime, meetPlace)


def set_goal(message, meetTime, meetPlace):
    cid = message.chat.id
    meetGoal = message.text
    # ToDo добавить место в БД
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Заполнить заново', callback_data='create'),
                 types.InlineKeyboardButton('Подтвердить', callback_data='accept'))
    bot.send_message(cid, 'Подтверждаете создание заявки: \n' +
                          'Время встречи: ' + meetTime + '\n'
                          'Место встречи: ' + meetPlace + '\n'
                          'Место обеда: ' + meetGoal + '\n',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'accept')
def create_handler(call):
    bot.send_message(call.message.chat.id, 'Ваша заявка добавлена')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
