import telebot
from telebot.types import Message
from telebot import types
from threading import Thread
import time
import schedule
import datetime
import dao
import userService
import lunchService

TOKEN = '1052618109:AAGCUts9_VvN97wyx8sKpii07eedU0F4mxw'
bot = telebot.TeleBot(TOKEN)

cities = ['Москва', 'Пермь', 'Челябинск', 'Омск', 'Уфа', 'Ижевск']

# {chat_id: city}
users = dict()

proc = None


def lunch_cleaner():
    now = datetime.datetime.now()
    lunchs = lunchService.getAll()
    for lunch in lunchs:
        splitted = lunch['time'].split(':')
        hours = int(splitted[0])
        minutes = int(splitted[1])
        lunch_time = datetime.datetime.now()
        lunch_time.replace(hour=hours, minute=minutes, second=0)
        if (now - lunch_time).total_seconds() // 60 == 15:
            users = userService.getAllByLunchId(lunch['id'])
            for user in users:
                bot.send_message(user.chat.id,
                                 "До обеда осталось 15 минут, встреча будет в " + lunch['place'] + ", людей записалось: " + str(
                                     len(users)))
        if now > lunch_time:
            print('Шедулер типо удоляет обед')
            lunchService.delete(lunch['id'])


schedule.every().minute.do(lunch_cleaner)


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
    global cities
    keyboard = types.InlineKeyboardMarkup()
    for city in cities:
        keyboard.add(types.InlineKeyboardButton(city, callback_data='add_city:' + city))
    bot.send_message(message.chat.id, "Выберите свой город",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'add_city' in call.data)
def city_setter(call):
    chat_id = call.message.chat.id
    city = call.data.split(':')[1]

    users[call.message.chat.id] = city
    if userService.findById(chat_id) is None:
        userService.add(chat_id, city, None)
    bot.send_message(chat_id,
                     "Вы выбрали город " + city + ", теперь ваши обеды будут проходить именно здесь!")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     "Приветствую " + name + ", я бот поиска компании для обедов. Если хочешь найти себе компанию, чтобы вместе вкусно поесть, ты попал по адресу.Всё что нужно это написать мне /lunch")


@bot.message_handler(commands=['lunch'])
def lunch_start(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Присоединиться', callback_data='join'),
                 types.InlineKeyboardButton('Предложить', callback_data='create'))
    bot.send_message(message.chat.id, "Вы хотите присоединиться к кому-то на обед или оставить свое предложение?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'join')
def join_handler(call):
    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
    bot.send_message(call.message.chat.id, 'Выберите одно из предложений на обед')
    lunchs = lunchService.getAllByUserId(call.message.chat.id)
    keyboard = types.InlineKeyboardMarkup()
    for lunch in lunchs:
        keyboard.add(types.InlineKeyboardButton(lunch['description'] + ' в ' + lunch['time'],
                                                callback_data='lunch_id:' + str(lunch['id'])))
    bot.send_message(call.message.chat.id, 'Выберите одно из предложений на обед', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'lunch_id' in call.data)
def join_handler(call):
    lunch_id = call.data.split(':')[1]
    userService.joinLunch(call.message.chat.id, lunch_id)


@bot.callback_query_handler(func=lambda call: call.data == 'create')
def create_handler(call):
    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
    msgTime = bot.send_message(call.message.chat.id, 'Введите время для обеда')
    bot.register_next_step_handler(msgTime, set_time)


def set_time(message):
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
            msgPlace = bot.send_message(cid, 'Введите место встречи')
            bot.register_next_step_handler(msgPlace, set_place, meetTime)

    else:
        msgTime = bot.send_message(message.chat.id, 'Введите корректное время')
        bot.register_next_step_handler(msgTime, set_time)


def set_place(message, meetTime):
    cid = message.chat.id
    meetPlace = message.text
    msgGoal = bot.send_message(cid, 'Введите описание обеда (желаемая пища/место)')
    bot.register_next_step_handler(msgGoal, set_goal, meetTime, meetPlace)


def set_goal(message, meetTime, meetPlace):
    cid = message.chat.id
    meetGoal = message.text
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Заполнить заново', callback_data='create'),
                 types.InlineKeyboardButton('Подтвердить', callback_data='accept'))
    lunchService.add(meetTime, cid, meetPlace, meetGoal)
    lunch = lunchService.findByOwnerId(cid)
    userService.joinLunch(cid, lunch['id'])
    bot.send_message(cid, 'Подтверждаете создание заявки: \n' +
                     'Время встречи: ' + meetTime + '\n'
                                                    'Место встречи: ' + meetPlace + '\n'
                                                                                    'Описание обеда: ' + meetGoal + '\n',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'accept')
def accept_handler(call):
    cid = call.message.chat.id
    bot.edit_message_reply_markup(cid, message_id=call.message.message_id, reply_markup='')
    bot.send_message(cid, 'Ваша заявка добавлена')


@bot.message_handler(commands=['check'])
def lunch_start(message):
    cid = message.chat.id
    lunch = lunchService.getActiveByUserId(cid)
    meetTime = lunch['time']
    meetPlace = lunch['place']
    meetGoal = lunch['description']
    if lunch is not None:
        bot.send_message(cid, 'Подтверждаете создание заявки: \n' +
                         'Время встречи: ' + meetTime + '\n'
                                                        'Место встречи: ' + meetPlace + '\n'
                                                                                        'Описание обеда: ' + meetGoal + '\n', )
    else:
        bot.send_message(cid, 'Вы не записаны на обед. Запишитесь или создайте заявку командой /lunch')


def main():
    dao.initDbTables()
    bot.polling()


if __name__ == '__main__':
    main()
