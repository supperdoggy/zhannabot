from constants import *
import random
import os
from data import *
import datetime

def start(chatId):
    if chatId == ZHANNA_ID:
        name = "зайка по имени Жанна"
    elif chatId == TATI_ID:
        name = "зайчик по имени Тати"
    elif chatId == NEMOKS_ID:
        name = "только не выключай меня создатель-господин"
    else:
        name = "зайка"

    return name

def getName(userid):
    if userid == TATI_ID:
        name = "Тати"
    elif userid == ZHANNA_ID:
        name = "Жанна"
    else:
        name = False

    return name

def getDanet():
    firstPart = ["Видимо ", "Точно ", "Я сказала ", "Походу ", 
                "Мне мама сказала что ", "Надеюсь что ", "Звезды сказали "]
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
            answer = "Ты уже узнал свой гороскоп на сегодня!"
    else:
        data = getData()
        answer = random.choice(data)

    return answer

def getAlcohol(chatId):
    if chatId == NEMOKS_ID:
        return "тільки водку, Макс, тільки водку..."

    types = ["Хватит пить!", "наливка в пьяной вишне", "наливка в белом наливе",
                "сидр", "глинтвейн", "вино", "шампанское", "джин-тоник", "ром-кола",
                "виски-кола", "рево", "лонгер", "рандомный коктейль",
                "шоты", "наливки", "самогоночку", "водочку", "все что нальют"]
    
    if chatId == ZHANNA_ID:
        types.append("что угодно только не водка жанна нет")
    elif chatId == TATI_ID:
        types.append("что угодно только не водка тати нет")

    answer = random.choice(types)

    return answer

def consoleOutput(message, answer):
    print("Мне написал человек с юзернеймом: %s" % message.from_user.username)
    print("Имя у него: %s" %message.from_user.first_name)
    print("Фамилия у него: %s" %message.from_user.last_name)
    print("Текст сообщения: %s" %message.text)
    print("Я ответила: %s" % answer)
    print("=" * 10)