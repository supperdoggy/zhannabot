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
        "never_have_I_ever": []
    }
    with open('data/%s.json' %message.from_user.id, 'w+') as outfile:
        json.dump(data, outfile)
    outfile.close()

def editLastTimePlayed(message):
    with open('data/%s.json' %message.from_user.id, 'r') as outfile:
        data = json.load(outfile)
    outfile.close()
    data["last_time_played_fortune"] = str(datetime.datetime.now().day)
    with open('data/%s.json' %message.from_user.id, 'w+') as outfile:
       json.dump(data, outfile)
    outfile.close()

def getLastTimePlayed(message):
    if not userExist(message.from_user.id):
        print("user doesnt exist")
        newUser(message)
        getLastTimePlayed(message)
    else:
        print("user exist")
        with open('data/%s.json' %message.from_user.id) as outfile:
            data = json.load(outfile)
        outfile.close()
        return data["last_time_played_fortune"]
