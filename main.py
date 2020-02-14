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
    name = start(message.chat.id)
    zhanna.send_message(message.chat.id, "Привет, %s" %name)

@zhanna.message_handler(commands=["fortune"])
def fortune(message):
    zhanna.send_message(message.chat.id, "%s" % getFortuneCookie(message))
    editLastTimePlayed(message)

@zhanna.message_handler(commands=["danet"])
def danet(message):
    zhanna.send_message(message.chat.id, "%s" % getDanet())

@zhanna.message_handler(commands=["somilye"])
def somilye(message):
    alcohol = getAlcohol(message.chat.id)
    if alcohol != "Хватит пить!":
        answer = "Сегодня мы пьем %s" % alcohol
    else:
        answer = "Хватит пить!"

    zhanna.send_message(message.chat.id, "%s" % answer)

@zhanna.message_handler(content_types=["text"])
def main(message):
    print(message)
    name = getName(message.chat.id)

    if name:
        if message.text.lower() == "у меня есть стрелки":
            zhanna.send_message(message.chat.id, "%s крутая!" % name)
        elif message.text.lower() == "у меня нету стрелок":
            zhanna.send_message(message.chat.id, "%s не очень крутая" % name)

zhanna.polling(none_stop=True)