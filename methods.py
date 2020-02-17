from constants import *
import random
import os
from data import *
import datetime
import apiai, json

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
    d = getLastTimePlayed(message)
    if str(datetime.datetime.now().day) != str(d):
        data = getData()
        answer = random.choice(data)
    else:
        answer = "Ты уже узнал свой гороскоп на сегодня!"

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
    storeAnswerAndQuestion(message, answer)

def getAnswer(message):
    name = getName(message.from_user.id)
    if name:
        if message.text.lower() == "у меня есть стрелки":
            answer = "%s крутая!" %name
            return answer
        elif message.text.lower() == "у меня нету стрелок":
            answer = "%s не очень крутая" % name
            return answer
    
    request = apiai.ApiAI(APIAITOKEN).text_request()
    request.lang = "ru"
    request.session_id = "zhanna"
    request.query = message.text
    responseJson = json.loads(request.getresponse().read().decode("utf-8"))
    answer = responseJson["result"]["fulfillment"]["speech"]
    
    if message.chat.type != "private":
        try:
            if message.text.lower().__contains__("жанна") or message.reply_to_message.from_user.id == 1058731629:
                if answer:
                    return answer
                else:
                    answer = message.text + "?"
                    return answer
        except:
            pass
    else:
        if answer:
            return answer
        else:
            answer = message.text + "?"
            return answer
    return None
