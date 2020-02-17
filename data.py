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

def userExist(id):
    return os.path.exists("data/%s.json"%id)

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
    writeData(message, data)

def editLastTimePlayed(message):
    data = readData(message)
    data["last_time_played_fortune"] = str(datetime.datetime.now().day)
    writeData(message, data)

def getLastTimePlayed(message):
    if not userExist(message.from_user.id):
        print("user doesnt exist")
        newUser(message)
        getLastTimePlayed(message)
    else:
        print("user exist")
        data = readData(message)
        return data["last_time_played_fortune"]

def storeAnswerAndQuestion(message, answer):
    if userExist(message.from_user.id):
        data = readData(message)

        data["questions"].append(message.text)
        data["answers"].append(answer)

        writeData(message, data)
    else:
        newUser(message)
        storeAnswerAndQuestion(message, answer)

def readData(message):
    with open('data/%s.json' %message.from_user.id) as outfile:
        data = json.load(outfile)
    outfile.close()
    return data

def writeData(message, data):
    with open('data/%s.json' %message.from_user.id, 'w+') as outfile:
        json.dump(data, outfile)
    outfile.close()

def appendNeverEver(message, answer):
    data = readData(message)
    data["never_have_I_ever"].append(answer)
    writeData(message, data)

def isInNeverEver(message, answer):
    data = readData(message)
    return answer in data["never_have_I_ever"]
    
