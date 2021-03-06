import random
import json
import datetime
import os
from constants.constants import *

# flowers

def writeToGraveYard(username, first_name, size):
    path = f"{FULL_PATH}{FLOWER_GRAVE_YARD_PATH}/lol.txt"
    try:
        f = open(path, "a+")
        lol = "="*10 + "\n" + "Время смерти: " + str(datetime.datetime.now()) + "\n" + "Имя пострадавшего: " + str(first_name) + "\n" + "Юзернейм пострадавшего: " + str(username) + "\n" + "Размер цветка: " + str(size) + "\n"
        f.write(lol)
        f.close()
    except:
        f = open(path, "w+")
        lol = "="*10 + "\n" + "Время смерти: " + str(datetime.datetime.now()) + "\n" + "Имя пострадавшего: " + str(first_name) + "\n" + "Юзернейм пострадавшего: " + str(username) + "\n" + "Размер цветка: " + str(size) + "\n"
        f.write(lol)
        f.close()

def getFlowerDataWithCheck(id):
    if userFlowerDataExist(id):
        return reatFlowerData(id)
    else:
        return None

def flowerChat(message):
    if userFlowerDataExist(message.chat.id):
        if userInFlowerChat(message.from_user.id, message.chat.id):
            pass
        else:
            appendUserInFlowerChat(message.from_user.id, message.chat.id)
    else:
        newFlowerChat(message)
        flowerChat(message)

def userFlowerDataExist(id):
    return True if os.path.exists(f"{FULL_PATH}{FLOWER_DATA_PATH}/{id}.json") else False

def userInFlowerChat(userId, chatId):
    return True if userId in reatFlowerData(chatId)["chat_users"] else False

def appendUserInFlowerChat(userId, chatId):
    data = reatFlowerData(chatId)
    data["chat_users"].append(userId)
    writeFlowerData(chatId, data)

def getFlowerData(message):
    if userFlowerDataExist(message.from_user.id):
        if message.chat.type != "private":
            flowerChat(message)
        return reatFlowerData(message.from_user.id)
    else:
        newFlower(message)
        return reatFlowerData(message.from_user.id)

def newFlowerChat(message):
    data = {
        "chat_username": message.chat.username,
        "chat_first_name": message.chat.first_name,
        "chat_id": message.chat.id,
        "chat_users": []
    }
    writeFlowerData(message.chat.id, data)

def newFlower(message):
    data = {
       "id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "last_time_played": (-1, -1, -1, -1), # year, month, day, hour
        "current_flower": 0,
        "total_amount_of_flowers": 0,
        "types":[]
    }
    writeFlowerData(message.from_user.id, data)


def writeFlowerData(id, data):
    with open(f"{FULL_PATH}{FLOWER_DATA_PATH}/{id}.json", "w+") as outfile:
        json.dump(data, outfile)
    outfile.close()

def reatFlowerData(id):
    with open(f"{FULL_PATH}{FLOWER_DATA_PATH}/{id}.json") as outfile:
        data = json.load(outfile)
    outfile.close()
    return data

# flowers

def getData():
    f = open(FULL_PATH + FORTUNE_DATA_PATH, "r")
    data = json.load(f)
    f.close()
    return data

def getTosts():
    f = open(FULL_PATH + TOSTS_DATA_PATH, "r")
    data = json.load(f)
    f.close()
    return data

def getNeverHaveIEver():
    f = open(FULL_PATH + NEVER_HAVE_I_EVER_DATA_PATH, "r")
    data = json.load(f)
    f.close()
    return data

def userInChat(message):
    if userExist(message.chat.id):
        data = readData(message.chat.id)
        for n in data["chat_users"]:
            if n["user_id"] == message.from_user.id:
                return True
        else:
            msg = {
                "user_id": message.from_user.id,
                "username": message.from_user.username
            }
            data["chat_users"].append(msg)
            writeData(message.chat.id, data)
    else:
        newChat(message)
        userInChat(message)

def userExist(id):
    return os.path.exists(f"{FULL_PATH}{CHAT_DATA_PATH}/{id}.json")

def newChat(message):
    if message.chat.type != "private":
        data = {
            "chat_username": message.chat.username,
            "chat_first_name": message.chat.first_name,
            "chat_id": message.chat.id,
            "chat_users": [],
            "antipara": "",
            "last_time_played_antipara": -1,
            "user_preb": "",
            "last_time_played_univer": -1
        }
        writeData(message.chat.id, data)

def newUser(message):
    if message.from_user.username == None:
        username = message.from_user.first_name
    else:
        username = message.from_user.username
    data = {
        "id": message.from_user.id,
        "username": username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "last_time_played_fortune": -1,
        "never_have_I_ever": [],
        "questions": [],
        "answers": []
    }
    writeData(message.from_user.id, data)

def editLastTimePlayed(message):
    data = readData(message.from_user.id)
    data["last_time_played_fortune"] = str(datetime.datetime.now().day)
    writeData(message.from_user.id, data)

def getLastTimePlayed(message):
    if not userExist(message.from_user.id):
        print("user doesnt exist")
        newUser(message)
        getLastTimePlayed(message)
    else:
        print("user exist")
        data = readData(message.from_user.id)
        return data["last_time_played_fortune"]

def storeLogs(data):
    logsDataPath = f"{FULL_PATH}{LOGS_PATH}/{str(datetime.date.today())}.txt"
    if os.path.exists(logsDataPath):
        open(logsDataPath, "a").write(data)
    else:
        open(logsDataPath, "w+").write(data)


def storeAnswerAndQuestion(message, answer):
    if userExist(message.from_user.id):
        data = readData(message.from_user.id)

        data["questions"].append(message.text)
        data["answers"].append(answer)

        writeData(message.from_user.id, data)
    else:
        newUser(message)
        storeAnswerAndQuestion(message, answer)

def readData(id):
    with open(f"{FULL_PATH}{CHAT_DATA_PATH}/{id}.json") as outfile:
        data = json.load(outfile)
    outfile.close()
    return data

def writeData(id, data):
    with open(f"{FULL_PATH}{CHAT_DATA_PATH}/{id}.json", 'w+') as outfile:
        json.dump(data, outfile)
    outfile.close()

def appendNeverEver(message, answer):
    data = readData(message.from_user.id)
    data["never_have_I_ever"].append(answer)
    writeData(message.from_user.id, data)

def isInNeverEver(message, answer):
    data = readData(message.from_user.id)
    return answer in data["never_have_I_ever"]

def userDataBase(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)