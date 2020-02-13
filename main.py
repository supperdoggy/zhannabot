import telebot
import random
from data import *
import os
import datetime
from constants import *
from methods import *

# TODO: rename bot from petya to zhanna idk....
# TODO: more functions
# TODO: more punk

petya = telebot.TeleBot(TOKEN)
@petya.message_handler(commands=["start"])
def greetings(message):
    if message.chat.id == ZHANNA_ID:
        petya.send_message(message.chat.id, "Привет, зайка по имени Жанна")
    
    elif message.chat.id == TATI_ID:
        petya.send_message(message.chat.id, "Привет, зайчик по имени Тати")
    
    else:
        petya.send_message(message.chat.id, "Привет, зайка")

@petya.message_handler(commands=["getall"])
def getAll(message):
    data = getData()
    for n in data:
        petya.send_message(message.chat.id, "%s" %n)

@petya.message_handler(commands=["fortune"])
def fortune(message):

    petya.send_message(message.chat.id, "%s" % getFortuneCookie(message))
    editLastTimePlayed(message)

@petya.message_handler(commands=["danet"])
def danet(message):
    petya.send_message(message.chat.id, "%s" % getDanet())

@petya.message_handler(content_types=["text"])
def main(message):
    print(message)
    name = getName(message.chat.id)

    if name:
        if message.text.lower() == "у меня есть стрелки":
            petya.send_message(message.chat.id, "%s крутая!" % name)
        elif message.text.lower() == "у меня нету стрелок":
            petya.send_message(message.chat.id, "%s не очень крутая" % name)

petya.polling(none_stop=True)