import random
import json
import datetime
import os

def getData():
    f = open("fortuneCookies.json", "r")
    data = json.load(f)
    return data

def getTosts():
    f = open("Tosts.json", "r")
    data = json.load(f)
    return data

def getNeverHaveIEver():
    f = open("neverever.json", "r")
    data = json.load(f)
    return data

def userInChat(message):
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

def userExist(id):
    return os.path.exists("data/%s.json"%id)

def newChat(message):
    if message.chat.type != "private":
        data = {
            "chat_username": message.chat.username,
            "chat_first_name": message.chat.first_name,
            "chat_id": message.chat.id,
            "chat_users": [],
            "last_time_played": -1
        }
        writeData(message.chat.id, data)

def newUser(message):
    data = {
        "id": message.from_user.id,
        "username": message.from_user.username,
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
    with open('data/%s.json' %id) as outfile:
        data = json.load(outfile)
    outfile.close()
    return data

def writeData(id, data):
    with open('data/%s.json' %id, 'w+') as outfile:
        json.dump(data, outfile)
    outfile.close()

def appendNeverEver(message, answer):
    data = readData(message.from_user.id)
    data["never_have_I_ever"].append(answer)
    writeData(message.from_user.id, data)

def isInNeverEver(message, answer):
    data = readData(message.from_user.id)
    return answer in data["never_have_I_ever"]
    
