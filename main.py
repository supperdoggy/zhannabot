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
    answer = "Привет, %s" %start(message.chat.id)
    zhanna.send_message(message.chat.id, "%s" %answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["fortune"])
def fortune(message):
    answer = getFortuneCookie(message)
    zhanna.send_message(message.chat.id, "%s" %answer)
    editLastTimePlayed(message)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["danet"])
def danet(message):
    answer = getDanet()
    zhanna.send_message(message.chat.id, "%s" % answer)
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["somilye"])
def somilye(message):
    alcohol = getAlcohol(message.chat.id)
    if alcohol != "Хватит пить!":
        answer = "Сегодня мы пьем %s" % alcohol
    else:
        answer = "Хватит пить!"
    zhanna.send_message(message.chat.id, "%s" % answer)
    consoleOutput(message, answer)

@zhanna.message_handler(content_types=["text"])
def main(message):
    print(message)
    name = getName(message.chat.id)

    if name:
        if message.text.lower() == "у меня есть стрелки":
            answer = "%s крутая!" %name
        elif message.text.lower() == "у меня нету стрелок":
            answer = "%s не очень крутая" % name
        zhanna.send_message(message.chat.id, "%s" %answer)
    consoleOutput(message, answer)

zhanna.polling(none_stop=True)