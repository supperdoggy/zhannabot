from constants import *
import random
import os
from data import *
import datetime

def getName(userid):
    if userid == TATI_ID:
        name = "Тати"
    elif userid == ZHANNA_ID:
        name == "Жанна"
    else:
        name = None

    return name

def getDanet():
    firstPart = ["Видимо ", "Точно ", "Я сказала ", "Походу "
                , "Мне мама сказала что ", "Надеюсь что ", "Звезды сказали "]
    secondPart = ["да", "нет"]
    answer = random.choice(firstPart) + random.choice(secondPart)
    return answer
def getFortuneCookie(message):
    if os.path.exists("data/%s.txt" % message.chat.id):
        d = getLastTimePlayed(message)
        if str(datetime.datetime.now().day) != str(d):
            data = getData()
            answer = random.choice(data)
        else:
            answer = "Ты уже узнал свой горокоп на сегодня!"
    else:
        data = getData()
        answer = random.choice(data)

    return answer