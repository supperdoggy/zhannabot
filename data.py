import random
import json
import datetime

def getData():

    f = open("fortuneCookies.json", "r")
    data = json.load(f)
    return data

def structuringData():
    with open("preds.txt") as f:
        lineList = f.readlines()
    f.close()

    for n in lineList:
        if n == "\n":
            lineList.remove(n)
    i = 0
    while i < len(lineList):
        if lineList[i] == "\n":
            lineList.remove(lineList[i])
        if i != 0:

            if lineList[i][0].islower():
                lineList[i-1] += " " + lineList[i]
                lineList.remove(lineList[i])
        i += 1
    return lineList

def editLastTimePlayed(message):
    f = open("data/%s.txt" % message.chat.id, "w+")
    f.write(str(datetime.datetime.now().day))
    f.close()

def getLastTimePlayed(message):
    f = open("data/%s.txt" % message.chat.id, "r")
    d = f.read()
    f.close()
    return d