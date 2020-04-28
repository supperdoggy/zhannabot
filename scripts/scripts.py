import json
import os
import random

def structuringData():
    with open(FULL_PATH + "preds.txt") as f:
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
    with open(FULL_PATH + "tosts.txt") as f:
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
    f = open(FULL_PATH + "Tosts.json", "w+")
    json.dump(lineList, f)

def structNeverEver():
    with open(FULL_PATH + "neverever.txt") as f:
        lineList = f.readlines()
    f.close()

    i = 0
    while i < len(lineList):
        if lineList[i] == "\n":
            lineList.pop(i)
        j = 0
        trash = ""
        for n in lineList[i]:
            if n != "Я":
                trash += n
            else:
                lineList[i] = lineList[i].replace("%s" %trash, "")
        i+=1

    with open(FULL_PATH + "neverever2.txt") as f:
        lineList2 = f.readlines()
    f.close()
    for n in lineList2:
        lineList.append(n)
    print(lineList)
    print(len(lineList))
    f = open("neverever.json", "w+")
    json.dump(lineList, f)

def structDate():
    with open(FULL_PATH + "date.txt") as f:
        string = f.read()
    f.close()
    i = 0
    lineList = []
    question = ""
    while i < len(string):
        if string[i] ==  "." or string[i] == "?":
            question+=string[i]
            lineList.append(question)
            question = ""
        else:
            question += string[i]
        i += 1
    lineList.pop(13)
    for n in lineList:
        print(n)
    
def getRandomFlowerType():
    types = ["🌱 Паросток", "🌹 Роза", "🥀 Роза которая спит", "🌷 Тюльпан", 
            "🌻 Подсолнух", "🌼 Гардения", "🌺 Азалия", "🌸 Адениум"]
    choice = random.choice(types)
    js = {
        "fullname": choice,
        "durability": 100,
        "icon": choice[0],
        "name": choice[2:]
    }
    return js

def structFlowerTypes():
    #{"id": 181474052, "username": "vikastrange", 
    # "first_name": "V", "last_name": null, 
    # "last_time_played": [2020, 4, 28, 0], 
    # "current_flower": 0, 
    # "total_amount_of_flowers": 25}
    lst = os.listdir(FULL_PATH+"flower_data")
    for n in lst:
        if n[0] == "-": continue
        dt = json.load(open(FULL_PATH+"flower_data/"+n,"r"))
        print(dt)
        js = {
            "id":dt["id"],
            "first_name":dt["first_name"],
            "username": dt["username"],
            "total_amount_of_flowers":dt["total_amount_of_flowers"],
            "types": [getRandomFlowerType() for n in range(dt["total_amount_of_flowers"])]

        }
        json.dump(js, open(FULL_PATH+"user-flower-types/%s"%n, "w+"))

if __name__ == "__main__":
    structFlowerTypes()