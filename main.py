import telebot
import random
from data import *
import os
import datetime
from constants import *
from methods import *
import apiai, json

# TODO: more punk
# TODO: maybe create minigame for chats like growing, feeding zhanna?

zhanna = telebot.TeleBot(TOKEN)
@zhanna.message_handler(commands=["start"])
def greetings(message):
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    answer = "Привет, %s" %start(message.from_user.id)
    zhanna.reply_to(message, "%s" %answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["fortune"])
def fortune(message):
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    answer = getFortuneCookie(message)
    zhanna.reply_to(message, "%s" %answer)
    editLastTimePlayed(message)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["antipara"])
def antipara(message):
    try:
        if message.chat.id != "private":
            data = readData(message.chat.id)
            if data["last_time_played"] != int(datetime.datetime.now().day):
                if len(data["chat_users"]) >= 2:
                    users = []
                    while True:
                        user = random.choice(data["chat_users"])
                        if user not in users:
                            users.append(user)
                        elif len(users) == 2:
                            break
                    data["last_time_played"] = int(datetime.datetime.now().day)
                    writeData(message.chat.id, data)
                    answer = "Антипара дня: @" + users[0]["username"] + " и  @" + users[1]["username"]
                    zhanna.reply_to(message, "%s" %answer)
                else:
                    answer = "У меня меньше двух зарегестрированых юзеров"
                    zhanna.reply_to(message, "%s"%answer)
            else:
                answer = "Антипара уже выбрана!"
                zhanna.reply_to(message, "%s" %answer)
            consoleOutput(message, answer)
    except:
        pass

@zhanna.message_handler(commands=["tost"])
def tost(message):
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    answer = random.choice(getTosts())
    zhanna.send_message(message.chat.id, "%s" %answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["danet"])
def danet(message):
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    answer = getDanet()
    zhanna.reply_to(message, "%s" % answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["somilye"])
def somilye(message):
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    alcohol = getAlcohol(message.from_user.id)
    if alcohol != "Хватит пить!":
        answer = "Сегодня мы пьем %s" % alcohol
    else:
        answer = "Хватит пить!"
    zhanna.reply_to(message, "%s" % answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["clear"])
def clear(message):
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    data = readData(message)
    data["never_have_I_ever"].clear()
    writeData(message, data)
    zhanna.reply_to(message, "Я удалила историю игры")

@zhanna.message_handler(commands=["neverhaveiever"])
def neverhaveiever(message):
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)

    answer = random.choice(getNeverHaveIEver())
    if isInNeverEver(message, answer):
        try:
            neverhaveiever(message)
        except:
            answer = getNeverHaveIEver()[0]

    zhanna.reply_to(message, "%s" %answer)
    appendNeverEver(message, answer)
    consoleOutput(message, answer)

@zhanna.message_handler(content_types=["text"])
def main(message):
    answer = getAnswer(message)
    if answer != None:
        zhanna.reply_to(message, "%s" %answer)
    if not userExist(message.from_user.id):
        newUser(message)
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    consoleOutput(message, answer)

zhanna.polling(none_stop=True)