import telebot
from telebot import types
from threading import Thread
import time
import datetime
import dao
import userService
import lunchService

TOKEN = '997103341:AAHEFEGSl6LF4JMxGZus6cMzcQLlhsaHOVQ'
bot = telebot.TeleBot(TOKEN)

cities = ['Москва', 'Пермь', 'Челябинск', 'Омск', 'Уфа', 'Ижевск']


def correct_hour_by_city(hour, city):
    result = hour
    if city == 'Москва':
        result = hour + 3
    elif city == 'Пермь':
        result = hour + 5
    elif city == 'Челябинск':
        result = hour + 5
    elif city == 'Омск':
        result = hour + 6
    elif city == 'Уфа':
        result = hour + 5
    elif city == 'Ижевск':
        result = hour + 4
    return result if result < 24 else result - 24


# {chat_id: city}
users = dict()

proc = None


def lunch_cleaner():
    time.sleep(5)
    while True:
        lunchs = lunchService.getAll()
        for lunch in lunchs:
            now = now_time_by_city(userService.findById(lunch['owner_id'])['city'])
            splitted = lunch['time'].split(':')
            hours = int(splitted[0])
            minutes = int(splitted[1])
            lunch_time = now.replace(hour=hours, minute=minutes, second=0)
            if (lunch_time - now).total_seconds() // 60 == 15:
                users_ids = userService.getAllByLunchId(lunch['id'])
                for user in users_ids:
                    try:
                        bot.send_message(user[0],
                                         "До обеда осталось 15 минут, встреча будет в " + lunch[
                                             'place'] + ", людей записалось: " + str(
                                             len(users_ids)))
                    except:
                        print('У мог бы упасть')
            if (lunch_time - now).total_seconds() < 0:
                users_ids = userService.getAllByLunchId(lunch['id'])
                for user in users_ids:
                    try:
                        bot.send_message(user[0],
                                         "Обед начался, встреча в " + lunch[
                                             'place'] + ", людей записалось: " + str(
                                             len(users_ids)))
                    except:
                        print('У мог бы упасть')
                lunchService.delete(lunch['id'])
        time.sleep(60)


def now_time_by_city(city):
    now = datetime.datetime.now(datetime.timezone.utc)
    now = now.replace(hour=correct_hour_by_city(now.hour, city))
    return now


Thread(target=lunch_cleaner, daemon=True).start()


@bot.message_handler(func=lambda message: message.chat.id not in users)
def kit_start(message):
    select_city(message)


@bot.message_handler(commands=['start'])
def city_change(message):
    select_city(message)


@bot.message_handler(commands=['time'])
def get_time(message):
    bot.send_message(message.chat.id, 'Сейчас времени: ' + now_time_by_city(users[message.chat.id]).strftime('%H:%M'))


def select_city(message):
    global cities
    keyboard = types.InlineKeyboardMarkup()
    for city in cities:
        keyboard.add(types.InlineKeyboardButton(city, callback_data='add_city:' + city))
    try:
        bot.send_message(message.chat.id, "Выберите свой город",
                         reply_markup=keyboard)
    except:
        print('У мог бы упасть')


@bot.callback_query_handler(func=lambda call: 'add_city' in call.data)
def city_setter(call):
    try:
        chat_id = call.message.chat.id
        city = call.data.split(':')[1]

        users[call.message.chat.id] = city
        if userService.findById(chat_id) is None:
            userService.add(chat_id, city, None)
        else:
            userService.updateCity(chat_id, city)
        bot.send_message(chat_id,
                         "Вы выбрали город " + city + ", теперь ваши обеды будут проходить именно здесь! Для создания обеда или если вы хотите присоединиться, введите /lunch")
    except:
        print('У мог бы упасть')


@bot.message_handler(commands=['help'])
def send_welcome(message):
    try:
        name = message.from_user.first_name
        bot.send_message(message.chat.id,
                         "Приветствую " + name + ", я бот поиска компании для обедов. Если хочешь найти себе компанию, чтобы вместе вкусно поесть, ты попал по адресу.Всё что нужно это написать мне /lunch")
    except:
        print('У мог бы упасть')


@bot.message_handler(commands=['lunch'])
def lunch_start(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Присоединиться', callback_data='join'),
                     types.InlineKeyboardButton('Предложить', callback_data='create'))
        bot.send_message(message.chat.id, "Вы хотите присоединиться к кому-то на обед или оставить свое предложение?",
                         reply_markup=keyboard)
    except:
        print('У мог бы упасть')


@bot.callback_query_handler(func=lambda call: call.data == 'join')
def join_handler(call):
    try:
        bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
        lunchs = lunchService.getAllByUserId(call.message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        for lunch in lunchs:
            keyboard.add(types.InlineKeyboardButton(lunch['description'] + ' в ' + lunch['time'],
                                                    callback_data='lunch_id:' + str(lunch['id'])))
        bot.send_message(call.message.chat.id, 'Выберите одно из предложений на обед', reply_markup=keyboard)
    except:
        print('У мог бы упасть')


@bot.callback_query_handler(func=lambda call: 'lunch_id' in call.data)
def join_handler(call):
    try:
        bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
        lunch_id = call.data.split(':')[1]
        userService.joinLunch(call.message.chat.id, lunch_id)
        bot.send_message(call.message.chat.id, 'Вы успешно присоединились к обеду!')
    except:
        print('У мог бы упасть')


@bot.callback_query_handler(func=lambda call: call.data == 'create')
def create_handler(call):
    try:
        bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
        msgTime = bot.send_message(call.message.chat.id, 'Введите время для обеда (формат ЧЧ:ММ)' +
                                   '--- Сейчас времени: ' + now_time_by_city(users[call.message.chat.id]).strftime(
            '%H:%M'))
        bot.register_next_step_handler(msgTime, set_time)
    except:
        print('У мог бы упасть')


def set_time(message):
    try:
        cid = message.chat.id
        meetTime = message.text
        if len(meetTime) == 5:
            ch = [char for char in meetTime]
            hour = ch[0] + ch[1]
            min = ch[3] + ch[4]
            if hour > '23' or hour < '0' or min > '59' or min < '0' or ch[2] != ':':
                msgTime = bot.send_message(message.chat.id, 'Введите корректное время')
                bot.register_next_step_handler(msgTime, set_time)
            else:
                msgPlace = bot.send_message(cid, 'Введите место встречи')
                bot.register_next_step_handler(msgPlace, set_place, meetTime)

        else:
            msgTime = bot.send_message(message.chat.id, 'Введите корректное время')
            bot.register_next_step_handler(msgTime, set_time)
    except:
        print('У мог бы упасть')


def set_place(message, meetTime):
    try:
        cid = message.chat.id
        meetPlace = message.text
        msgGoal = bot.send_message(cid, 'Введите описание обеда (желаемая пища/место)')
        bot.register_next_step_handler(msgGoal, set_goal, meetTime, meetPlace)
    except:
        print('У мог бы упасть')


def set_goal(message, meetTime, meetPlace):
    try:
        cid = message.chat.id
        meetGoal = message.text
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Заполнить заново', callback_data='create'),
                     types.InlineKeyboardButton('Подтвердить', callback_data='accept'))
        lunchService.add(meetTime, cid, meetPlace, meetGoal)
        lunch = lunchService.findByOwnerId(cid)
        userService.joinLunch(cid, lunch['id'])
        bot.send_message(cid, 'Подтверждаете создание заявки:\n\n' +
                         'Время встречи: ' + meetTime + '\n' +
                         'Место встречи: ' + meetPlace + '\n' +
                         'Описание обеда: ' + meetGoal + '\n' +
                         '--- Сейчас времени: ' + now_time_by_city(users[message.chat.id]).strftime('%H:%M'),
                         reply_markup=keyboard)
    except:
        print('У мог бы упасть')


@bot.callback_query_handler(func=lambda call: call.data == 'accept')
def accept_handler(call):
    try:
        cid = call.message.chat.id
        bot.edit_message_reply_markup(cid, message_id=call.message.message_id, reply_markup='')
        bot.send_message(cid,
                         'Ваша заявка добавлена, вы всегда можете посмотреть сколько сейчас времени командой /time')
    except:
        print('У мог бы упасть')


@bot.message_handler(commands=['check'])
def lunch_start(message):
    try:
        cid = message.chat.id
        lunch = lunchService.getActiveByUserId(cid)
        if lunch is not None:
            meetTime = lunch['time']
            meetPlace = lunch['place']
            meetGoal = lunch['description']
            bot.send_message(cid, 'Вы записаны на обед: \n\n' +
                             'Время встречи: ' + meetTime + '\n' +
                             'Место встречи: ' + meetPlace + '\n' +
                             'Описание обеда: ' + meetGoal + '\n' +
                             '--- Сейчас времени: ' + now_time_by_city(users[message.chat.id]).strftime('%H:%M'))
        else:
            bot.send_message(cid, 'Вы не записаны на обед. Запишитесь или создайте заявку командой /lunch')
    except:
        print('У мог бы упасть')


def main():
    dao.initDbTables()
    bot.polling()


if __name__ == '__main__':
    main()
