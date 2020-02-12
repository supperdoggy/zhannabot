import telebot
import random
from data import *
import os
import datetime
from constants import *

petya = telebot.TeleBot(TOKEN)
@petya.message_handler(commands=["start"])
def greetings(message):
    petya.send_message(message.chat.id, "Привет, zhanna")

@petya.message_handler(commands=["getall"])
def getAll(message):
    data = getData()
    for n in data:
        petya.send_message(message.chat.id, "%s" %n)

@petya.message_handler(commands=["fortune"])
def fortune(message):
    try:
        if os.path.exists("data/%s.txt" % message.chat.id):
            d = getLastTimePlayed()
            if str(datetime.datetime.now().day) != str(d):
                data = getData()
                answer = random.choice(data)
                petya.send_message(message.chat.id,  "%s" % answer)

            else:
                petya.send_message(message.chat.id, "Ты уже играл сегодня!")
        else:
            data = getData()
            answer = random.choice(data)
            petya.send_message(message.chat.id,  "%s" % answer)
        
    except:
        pass
    editLastTimePlayed(message)

@petya.message_handler(commands=["danet"])
def danet(message):
    firstPart = ["Видимо ", "Точно ", "Я сказал ", "Походу "
    , "Мне мама сказала что ", "Надеюсь что ", "Звезды сказали "]
    secondPart = ["да", "нет"]
    answer = random.choice(firstPart) + random.choice(secondPart)
    petya.send_message(message.chat.id, "%s" %answer)

@petya.message_handler(content_types=["text"])
def main(message):
    print(message)
    if message.text.lower() == "у меня есть стрелки":
        petya.send_message(message.chat.id, "Жанна крутая!")
    elif message.text.lower() == "у меня нету стрелок":
        petya.send_message(message.chat.id, "Жанна не очень крутая")
    else:
        petya.send_message(message.chat.id, "Я понимаю только:\nУ меня есть стрелки\nУ меня нету стрелок")

petya.polling(none_stop=True)