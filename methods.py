from constants import ZHANNA_ID, TATI_ID, NEMOKS_ID, BOT_ID, CHANCE_OF_DYING_FLOWER
import random
import os
from data import *
import datetime
from ml import *
from access import isBanned

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
    d = getLastTimePlayed(message) # d - day
    if str(datetime.datetime.now().day) != str(d):
        data = getData()
        answer = random.choice(data)
    else:
        answer = "Ты уже узнал свой гороскоп на сегодня!"

    return answer

def getAlcohol(chatId):
    types = ["Хватит пить!", "наливка в пьяной вишне", "наливка в белом наливе",
                "сидр", "глинтвейн", "вино", "шампанское", "джин-тоник", "ром-кола",
                "виски-кола", "рево", "лонгер", "рандомный коктейль",
                "шоты", "наливки", "самогоночку", "водочку", "все что нальют"]
    
    if chatId == NEMOKS_ID:
        types.append("тільки водку, Макс, тільки водку...")
    elif chatId == ZHANNA_ID:
        types.append("что угодно только не водка жанна нет")
    elif chatId == TATI_ID:
        types.append("что угодно только не водка тати нет")

    alcohol = random.choice(types)

    if alcohol != types[0]: #types[0] - "Хватит пить!"
        return "Сегодня мы пьем %s" % alcohol
    else:
        return "Хватит пить!"

def consoleOutput(message, answer):
    print("Мне написал человек с юзернеймом: %s" % message.from_user.username)
    print("Имя у него: %s" %message.from_user.first_name)
    print("Фамилия у него: %s" %message.from_user.last_name)
    print("Юзер забанен: %s" % isBanned(message.from_user.id))
    print("Текст сообщения: %s" %message.text)
    print("Я ответила: %s" % answer)
    print("Время: %s"%datetime.datetime.now())
    print("=" * 10)
    storeAnswerAndQuestion(message, answer)

def getTostAnswer():
    return random.choice(getTosts())

def sendingAnswer(id, answer):
    answer = answerCheck(answer)
    if isBanned(id):
        if answer.lower().__contains__("@"):
            return answer.replace("@rarezhanna", "меня")
    return answer

# TODO: refactore code!
def getAnswer(message):
    # Firstly it checks the user id is tati`s or zhanna`s id
    name = getName(message.from_user.id)
    if name:
        # and then it checs if 
        if message.text.lower().__contains__("у меня есть стрелки"):
            answer = "%s крутая!" %name
            return answer
        elif message.text.lower().__contains__("у меня нету стрелок"):
            answer = "%s не очень крутая" % name
            return answer

    answer = getApiAiAnswer(message)

    if message.chat.type != "private":
        if message.reply_to_message.from_user.id == BOT_ID:
            return sendingAnswer(message.from_user.id, answer)
    else:
        return sendingAnswer(message.from_user.id, answer)
    return None

# TODO: refactor this part of code
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
                # returning previous antipara without "@" to avoid tagging people
                return "Антипара уже выбрана!\n" + data["antipara"].replace("@", "")
        # if chat doesnt exist in then add it
        else:
            # creating base for chat
            newChat(message)
            # recursion this method
            getAntipara(message)
    else:
        # if chat is public then returning None
        return None

# flower

def canGrowFlower(data):
    date = datetime.datetime.now()

    # 0 - year
    # 1 - month
    # 2 - day
    # 3 - hour
    if data["last_time_played"][0] < date.year:
        return True
    elif data["last_time_played"][1] < date.month:
        return True
    elif data["last_time_played"][2] < date.day:
        return True
    elif data["last_time_played"][3] + 6 <= date.hour:
        return True
    return False

def flowerDies():
    return True if random.randint(0, 100) <= CHANCE_OF_DYING_FLOWER else False

def editLastTimePlayedFlower(data):
    date = datetime.datetime.now()
    data["last_time_played"][0] = date.year
    data["last_time_played"][1] = date.month
    data["last_time_played"][2] = date.day
    data["last_time_played"][3] = date.hour
    return data

def flower(message):
    data = getFlowerData(message)
    if canGrowFlower(data):
        if flowerDies():
            data["current_flower"] = 0
            answer = "йой, кажется твой цветочек умер, обнуляем результаты"
        else:
            data["current_flower"] += random.randint(0, 10)
            if data["current_flower"] >= 100:
                data["total_amount_of_flowers"] += 1
                data["current_flower"] = 0
                answer = "Твой цветочек уже вырос! у тебя уже %s цветоков"%data["total_amount_of_flowers"]  
            else:
                answer = "У твоего цветочка уже %s цветочных баллов" %data["current_flower"] 
    
        data = editLastTimePlayedFlower(data)
        # saving changes
        writeFlowerData(message.from_user.id, data)

        return answer
    else:
        return "цветочки не растут так часто, их можно растить раз в 6 часов"

def getFlowers(message):
    data = getFlowerData(message)
    return "У тебя уже " + str(data["total_amount_of_flowers"]) + " вырощенных цветочков! А у цветочка, который ты выращиваешь сейчас - " + str(data["current_flower"]) + " цветочковых баллов."

def bubble(array, array2):
    for i in range(len(array)-1):
        for j in range(len(array)-i-1):
            if array[j] < array[j+1]:
                buff = array[j]
                buff1 = array2[j]
                array[j] = array[j+1]
                array[j+1] = buff
                array2[j] = array2[j+1]
                array2[j+1] = buff1

# TODO: holy fuck just refactor this pizdec
def getTopFlowers(message):
    try:
        if message.chat.type != "private":
            data = getFlowerData(message)
            chatData = reatFlowerData(message.chat.id)

            data_list = []
            for n in chatData["chat_users"]:
                if userFlowerDataExist(n):
                    data = reatFlowerData(n)
                    data_list.append(data)

            usernames = []
            sizes = []
            i = 0
            while i < len(data_list):
                usernames.append(data_list[i]["username"])
                sizes.append(data_list[i]["total_amount_of_flowers"] * 100  + data_list[i]["current_flower"])
                i+=1

            bubble(sizes, usernames)

            i = 0
            answer = ""
            while i<len(sizes):
                answer += str(i+1) + ": " + str(usernames[i]) + str(" - ") + str(round(sizes[i]/100)) +" цветочков и " + str(sizes[i] - (round(sizes[i]/100) * 100)) + " цветочковых единиц\n"
                i+=1
            
            return answer
        else:
            return "Это не паблик чат"
    except:
        return "Лол я умерла"