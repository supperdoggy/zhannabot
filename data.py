import random
import json
import datetime

def getData():
    f = open("fortuneCookies.json", "r")
    data = json.load(f)
    return data

def getTosts():
    f = open("Tosts.json", "r")
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

def structuringTosts():
    with open("tosts.txt") as f:
        lineList = f.readlines()
    f.close()
    i = 0
    while i<len(lineList):
        if lineList[i] == "\n":
            lineList.remove(lineList[i])
        if lineList[i].__contains__("\n"):
            lineList[i] = lineList[i].replace("\n", "")
        if lineList[i].__contains__("*"):
            lineList.remove(lineList[i])
        i+=1
    i=0
    while i<len(lineList):
        if lineList[i] == "\n":
            lineList.pop(i)
        i+=1
    i=0
    while i<len(lineList):
        if lineList[i] == "\n":
            lineList.pop(i)
        i+=1

    names = ["Егора", "Женю", "енотов", "обезьян", "слонов", "тигров", "Максима", "собак", "пиво", "любовь!", "лил пипа",
            "алкоголь", "любимую печень", "баб сисястых и нас глазастых", "игуан", "африку", "панков"]
    i = 0
    while i < len(names):
        tost = "Выпьем за " + names[i]
        lineList.append(tost)
        i+=1

    i = 0
    while i < len(lineList):
        if lineList[i] == "":
            lineList.pop(i)
        i+=1

    print(len(lineList))
    f = open("Tosts.json", "w+")
    json.dump(lineList, f)


 
def editLastTimePlayed(message):
    f = open("data/%s.txt" % message.from_user.id, "w+")
    f.write(str(datetime.datetime.now().day))
    f.close()

def getLastTimePlayed(message):
    f = open("data/%s.txt" % message.chat.id, "r")
    d = f.read()
    f.close()
    return d

if __name__ == "__main__":
    structuringTosts()