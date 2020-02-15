import telebot
import random
from data import *
import os
import datetime
from constants import *
from methods import *

# TODO: more punk

zhanna = telebot.TeleBot(TOKEN)
@zhanna.message_handler(commands=["start"])
def greetings(message):
    answer = "Привет, %s" %start(message.from_user.id)
    zhanna.reply_to(message, "%s" %answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["fortune"])
def fortune(message):
    answer = getFortuneCookie(message)
    zhanna.reply_to(message, "%s" %answer)
    editLastTimePlayed(message)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["tost"])
def tost(message):
    answer = random.choice(getTosts())
    zhanna.send_message(message.chat.id, "%s" %answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["danet"])
def danet(message):
    answer = getDanet()
    zhanna.reply_to(message, "%s" % answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["somilye"])
def somilye(message):
    alcohol = getAlcohol(message.from_user.id)
    if alcohol != "Хватит пить!":
        answer = "Сегодня мы пьем %s" % alcohol
    else:
        answer = "Хватит пить!"
    zhanna.reply_to(message, "%s" % answer)
    consoleOutput(message, answer)

@zhanna.message_handler(content_types=["text"])
def main(message):
    name = getName(message.chat.id)
    answer = None

    if name:
        if message.text.lower() == "у меня есть стрелки":
            answer = "%s крутая!" %name
        elif message.text.lower() == "у меня нету стрелок":
            answer = "%s не очень крутая" % name
        zhanna.reply_to(message, "%s" %answer)
    consoleOutput(message, answer)

zhanna.polling(none_stop=True)