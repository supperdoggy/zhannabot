from constants import *
import random
import os
from data import *
import datetime
from ml import *

def start(chatId):
    if chatId == ZHANNA_ID:
        name = "зайка по имени Жанна"
    elif chatId == TATI_ID:
        name = "зайчик по имени Тати"
    elif chatId == NEMOKS_ID:
        name = "только не выключай меня создатель-господин"
    else:
        name = "зайка"
    answer = "Привет, %s" %name
    return answer

def getNHIEAnswer(message):
    answer = random.choice(getNeverHaveIEver())
    if isInNeverEver(message, answer):
        try:
            getNHIEAnswer(message)
        except:
            return getNeverHaveIEver()[0]
    return answer

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

    alcohol = random.choice(types)

    if alcohol != "Хватит пить!":
        return "Сегодня мы пьем %s" % alcohol
    else:
        return "Хватит пить!"

def consoleOutput(message, answer):
    print("Мне написал человек с юзернеймом: %s" % message.from_user.username)
    print("Имя у него: %s" %message.from_user.first_name)
    print("Фамилия у него: %s" %message.from_user.last_name)
    print("Текст сообщения: %s" %message.text)
    print("Я ответила: %s" % answer)
    print("=" * 10)
    storeAnswerAndQuestion(message, answer)

def getTostAnswer():
    return random.choice(getTosts())

def getAnswer(message):
    name = getName(message.from_user.id)
    if name:
        if message.text.lower() == "у меня есть стрелки":
            answer = "%s крутая!" %name
            return answer
        elif message.text.lower() == "у меня нету стрелок":
            answer = "%s не очень крутая" % name
            return answer
    
    answer = getApiAiAnswer(message)

    if message.chat.type != "private":
        if message.reply_to_message.from_user.id == BOT_ID:
            if answer:
                return answer
            else:
                return IDontUnderstand()
    else:
        if answer:
            return answer
        else:
            return IDontUnderstand()
    return None

# TODO: refactoring this part of code
# calculating answer for antipara command
def getAntipara(message):
    # works only in public chats
    # check for chat type
    if message.chat.type != "private":
        # check if chat exist in base
        if userExist(message.chat.id):
            # getting chat data
            data = readData(message.chat.id)
            # you can only play it once per day
            if data["last_time_played_antipara"] != int(datetime.datetime.now().day):
                # check if there is at least 2 registered chat users
                if len(data["chat_users"]) >= 2:
                    # list which will contain two random chosen users
                    pair = []
                    while len(pair) != 2:
                        # random choice from registered chat users
                        user = random.choice(data["chat_users"])
                        # check if there are the same user in pair
                        if user not in pair:
                            # if not then append it into the pair
                            pair.append(user)
                    # changing last time played
                    data["last_time_played_antipara"] = int(datetime.datetime.now().day)
                    # changing antipara of the day
                    data["antipara"] = "Антипара дня: @" + pair[0]["username"] + " и  @" + pair[1]["username"]
                    # saving chat data
                    writeData(message.chat.id, data)
                    # returning antipara of the day
                    return data["antipara"]
                else:
                    return "У меня меньше двух зарегестрированых юзеров"
            else:
                # returning previous antipara
                return "Анти пара уже выбрана!\n" + data["antipara"]
        # if chat doesnt exist in then add it
        else:
            # creating base for chat
            newChat(message)
            # recursion this method
            getAntipara(message)
    else:
        # if chat is public then returning None
        return None
