from constants import ZHANNA_ID, TATI_ID, NEMOKS_ID, BOT_ID
from cfg import *
import random
import os
from data import *
import datetime
from ml import *
from access import isBanned

def zhannaReplies(zhanna, message, answer):
    try:
        if answer != None:
            zhanna.reply_to(message, "%s"%answer)
    except:
        pass

# ====================== sending answer to start command ======================

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

# ====================== sending answer to start command ======================

# ====================== sending random NHIE from json file ======================

def getNHIEAnswer(message):
    answer = random.choice(getNeverHaveIEver())
    if isInNeverEver(message, answer):
        try:
            getNHIEAnswer(message)
        except:
            return getNeverHaveIEver()[0]
    return answer
# ====================== sending random NHIE from json file ======================

# ====================== sending random yes or no ======================

def getDanet():
    firstPart = ["Видимо ", "Точно ", "Я сказала ", "Походу ", 
                "Мне мама сказала что ", "Надеюсь что ", "Звезды сказали "]
    secondPart = ["да", "нет"]
    answer = random.choice(firstPart) + random.choice(secondPart)
    return answer

# ====================== sending random yes or no ======================

# ====================== sending random fortune cookie from json file ======================

def getFortuneCookie(message):
    d = getLastTimePlayed(message) # d - day
    if str(datetime.datetime.now().day) != str(d):
        data = getData()
        answer = random.choice(data)
    else:
        answer = "Ты уже узнал свой гороскоп на сегодня!"

    return answer

# ====================== sending random fortune cookie from json file ======================

# ====================== sending alcohol ======================

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

# ====================== sending alcohol ======================

# ====================== logs ======================

def consoleOutput(message, answer):
    print("Мне написал человек с юзернеймом: %s" % message.from_user.username)
    print("Имя у него: %s" %message.from_user.first_name)
    print("Фамилия у него: %s" %message.from_user.last_name)
    print("Юзер забанен: %s" % isBanned(message.from_user.id))
    print("Текст сообщения: %s" %message.text)
    print("Я ответила: %s" % answer)
    print("Время: %s"%datetime.datetime.now())
    print("=" * 10)
    try:
        storeAnswerAndQuestion(message, answer)
    except:
        pass

# ====================== logs ======================

# ====================== sending random tost from json file ======================

def getTostAnswer():
    return random.choice(getTosts())

# ====================== sending random tost from json file ======================

# ====================== answer when user writes text ======================

def sendingAnswer(id, answer):
    answer = answerCheck(answer)
    if isBanned(id):
        if answer.lower().__contains__("@"):
            return answer.replace("@rarezhanna", "меня")
    return answer

def getName(userid):
    if userid == TATI_ID:
        name = "Тати"
    elif userid == ZHANNA_ID:
        name = "Жанна"
    else:
        name = False

    return name

def getAnswer(message):
    # First of all it checks the user id is tati`s or zhanna`s id
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
# ====================== answer when user writes text ======================

# ====================== pair of antipara ======================

def moreThanTwoUsersInChat(data):
    return True if len(data["chat_users"]) >= 2 else False

def canPlayAntipara(data):
    return True if data["last_time_played_antipara"] != int(datetime.datetime.now().day) else False

def getAntipara(message):
    if message.chat.type == "private":
        return None

    if not userExist(message.chat.id):
        # creating base for chat
        newChat(message)
        # recursion this method
        getAntipara(message)

    # getting chat data    
    data = readData(message.chat.id)
    # returning previous antipara without "@" to avoid tagging people
    if not canPlayAntipara(data):
        return "Антипара уже выбрана!\n" + data["antipara"].replace("@", "")
    
    if not moreThanTwoUsersInChat(data):
        return "У меня меньше двух зарегестрированых юзеров"
    
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
# ====================== pair of antipara ======================

# ====================== randomly picked one user ======================
# TODO: refactor it
def getCorona(message):
# works only in group chats
    if message.chat.type != "private":
        # checks if chat exist
        if userExist(message.chat.id):
            # getting data
            data = readData(message.chat.id)
            # you can only play once per day
            if data["last_time_played_univer"] != int(datetime.datetime.now().day):
                # getting new random user
                user = random.choice(data["chat_users"])
                data["user_proeb"] = "Сегодня @%s сто проц не умрет, наслаждайся этим днем!" %user["username"]
                # editing last time played
                data["last_time_played_univer"] = int(datetime.datetime.now().day)
                # saving changes
                writeData(message.chat.id, data)
                # getting answer
                return data["user_proeb"]
            else:
                # deleting "@", to avoid tagging user
                return "Сегодня уже выбрали одного счасливчика, пока хватит\n" + data["user_proeb"].replace("@", "")
    else:
        # if chat type is private then bot doesnt send answer
        return "Это работает только в публичных группах"
# ====================== randomly picked one user ======================

# ====================== growing flower ======================

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
    elif data["last_time_played"][3] + GROWING_TIME_LIMIT <= date.hour:
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

def flowerGrows(currentSize, userId):
    try:
        amountOfMessages = len(readData(userId)["questions"])
    except:
        amountOfMessages = 0
    extra = int(amountOfMessages *  MESSAGE_MULTIPLYER)
    extra = extra if extra <=20 else 20
    currentSize += random.randint(LOWER_RANDOM_FLOWER_NUMBER, HIGHER_RANDOM_FLOWER_NUMBER) + extra
    return int(currentSize)

def getExtra(userId):
    try:
        amountOfMessages = len(readData(userId)["questions"])
    except:
        amountOfMessages = 0
    extra = int(amountOfMessages *  MESSAGE_MULTIPLYER)
    return extra if extra<=20 else 20

def whenCanGrowAgain(time):
    for _ in range(GROWING_TIME_LIMIT+2+1+3):# +3 cos of time difference
        if time<24:
            time+=1
        else:
            time=0
    return time


def flower(message):
    data = getFlowerData(message)
    if not canGrowFlower(data):
        return "цветочки не растут так часто, их можно растить раз в 6 часов, попробуй еще раз в %s:00" %whenCanGrowAgain(data["last_time_played"][3])

    if flowerDies():
        writeToGraveYard(data["username"], data["first_name"], data["current_flower"])
        data["current_flower"] = 0
        answer = "йой, кажется твой цветочек умер, обнуляем результаты"
    else:
        data["current_flower"] = flowerGrows(data["current_flower"], data["id"])

        if data["current_flower"] >= 100:
            data["total_amount_of_flowers"] += 1
            data["current_flower"] = 0
            answer = "Твой цветочек уже вырос! у тебя уже %s цветочков"%data["total_amount_of_flowers"]  

        else:
            answer = "У твоего цветочка уже %s цветочных баллов" %data["current_flower"] 
    
    data = editLastTimePlayedFlower(data)
    # saving changes
    writeFlowerData(message.from_user.id, data)

    return answer

# ====================== growing flower ======================

# ====================== get flower data to user ======================

def getFlowers(message):
    data = getFlowerData(message)
    return "У тебя уже " + str(data["total_amount_of_flowers"]) + " вырощенных цветочков! А у цветочка, который ты выращиваешь сейчас " + str(data["current_flower"]) + f" цветочковых баллов.\n\nДополнительный прирост: {getExtra(data['id'])}"

# ====================== get flower data to user ======================

# ====================== top flowers in chat ======================
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

def buildTopFlowersAnswer(data_list, sizes, usernames):
    i = 0
    answer = ""
    while i<len(sizes):
        for n in data_list:
            if n["username"] == usernames[i]:
                flowers = n["total_amount_of_flowers"]
                current = n["current_flower"]
        answer += str(i+1) + ": " + str(usernames[i]) + str(" - ") + str(flowers) +" 🌷, " + str(current) + "🌱\n"
        i+=1

    return answer

def getUsersData(chatUsers):
    data_list = []
    for n in chatUsers:
        if userFlowerDataExist(n):
            data = reatFlowerData(n)
            data_list.append(data)

    return data_list

# TODO: holy fuck just refactor this pizdec
def getTopFlowers(message):
    if message.chat.type == "private":
        return "Это не паблик чат"
    
    data = getFlowerData(message)
    chatData = reatFlowerData(message.chat.id)

    data_list = getUsersData(chatData["chat_users"])

    usernames = []
    sizes = []
    i = 0
    while i < len(data_list):
        usernames.append(data_list[i]["username"])
        sizes.append(data_list[i]["total_amount_of_flowers"] * 100  + data_list[i]["current_flower"])
        i+=1

    bubble(sizes, usernames)
            
    return buildTopFlowersAnswer(data_list, sizes, usernames)

# ====================== top flowers in chat ======================

# ====================== sending flowers ======================

def userCanGive(flowers, amount):
    return True if flowers>amount else False

def sendFlower(message, amount=1):
    if message.chat.type == "private":
        return "Работает только в паблик чатах"
    # from
    idUserOne = message.from_user.id
    # to
    if message.reply_to_message != None:
        idUserTwo = message.reply_to_message.from_user.id
    else:
        return "Ответь на сообщение того кому хочешь подарить цветок!"

    if idUserOne == idUserTwo:
        return "Нахуй  иди ок? Багоюзер ебаный"

    # getting user one data
    dataUserOne = getFlowerDataWithCheck(idUserOne)
    if dataUserOne == None:
        return "Тебя нету в мое базе("

    # getting user two data
    dataUserTwo = getFlowerDataWithCheck(idUserTwo)
    if dataUserTwo == None:
        return "Этого пользователя нету в мое базе("
    
    if not userCanGive(dataUserOne["total_amount_of_flowers"], amount):
        return "У тебя нету цветков!"

    # adding flower
    dataUserTwo["total_amount_of_flowers"]+=amount
    # removing flower
    dataUserOne["total_amount_of_flowers"]-=amount
    
    # saving changes
    writeFlowerData(idUserOne, dataUserOne)
    writeFlowerData(idUserTwo, dataUserTwo)

    return f"Ты успешно подарил 1 цветок!\nУ тебя осталось еще {dataUserOne['total_amount_of_flowers']} цветков!"

# ====================== sending flowers ======================
