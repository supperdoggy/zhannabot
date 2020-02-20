import telebot
import random
from data import *
import os
import datetime
from constants import *
from methods import *
import apiai, json

# TODO: more punk
# TODO: maybe create minigame for chats like growing, feeding zhanna?
# TODO: Прогульщик дня

# start command
zhanna = telebot.TeleBot(TOKEN)
@zhanna.message_handler(commands=["start"])
def greetings(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    # getting greetings message
    answer = start(message.from_user.id)
    # zhanna replies to message
    zhanna.reply_to(message, "%s" %answer)
    # console output for administration
    consoleOutput(message, answer)

# command for getting personal fortune cookie
@zhanna.message_handler(commands=["fortune"])
def fortune(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    # getting fortune cookie for user
    answer = getFortuneCookie(message)
    # zhanna answering
    zhanna.reply_to(message, "%s" %answer)
    # edditing the last time played
    editLastTimePlayed(message)
    # console output for administration
    consoleOutput(message, answer)

# antipara command
@zhanna.message_handler(commands=["antipara"])
def antipara(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    # getting antipara
    answer = getAntipara(message)
    # answer is not None than zhanna answer to the command
    if answer:
        zhanna.reply_to(message, "%s"%answer)
    # console output for administration
    consoleOutput(message, answer)

# TODO: finish it
# TODO: TEST IT!
@zhanna.message_handler(commands=["proebat"])
def proebat(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    
    # works only in group chats
    if message.chat.type != "private":
        # checks if chat exist
        if userExist(message.chat.id):
            # getting data
            data = readData(message.chat.id)
            # you can only play once per day
            if data["last_time_played_univer"] != int(datetime.datetime.now().day):
                # getting new random user
                data["user_proeb"] = "Сегодня @%s может спокойно проебать на пары" %random.choice(data["users"]["username"])
                # editing last time played
                data["last_time_played_univer"] = int(datetime.datetime.now().day)
                # saving changes
                writeData(message.chat.id, data)
            # getting answer
            answer = data["user_proeb"]
    else:
        # if chat type is private then bot doesnt send answer
        answer = ""
    # zhanna replies to user with answer
    zhanna.reply_to(message, "%s"%answer)
    
# command for getting cheer tost
@zhanna.message_handler(commands=["tost"])
def tost(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    # getting random tost as an answer for user
    answer = getTostAnswer()
    # replying to user
    zhanna.send_message(message.chat.id, "%s" %answer)
    # console output for administration
    consoleOutput(message, answer)

# command for getting random yes or no
@zhanna.message_handler(commands=["danet"])
def danet(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    # getting answer
    answer = getDanet()
    # replying to user
    zhanna.reply_to(message, "%s" % answer)
    # console output for administration
    consoleOutput(message, answer)

# command for getting random drink
@zhanna.message_handler(commands=["somilye"])
def somilye(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    # getting random drink for user
    answer = getAlcohol(message.from_user.id)
    # replying to user
    zhanna.reply_to(message, "%s" % answer)
    # console output for administration
    consoleOutput(message, answer)

# never have i ever command
@zhanna.message_handler(commands=["neverhaveiever"])
def neverhaveiever(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)

    # getting random neverHaveIEver statement
    answer = getNHIEAnswer(message)
    # replying to user
    zhanna.reply_to(message, "%s" %answer)
    # appending new statement into the history
    appendNeverEver(message, answer)
    # console output for administration
    consoleOutput(message, answer)

# hidden command for clearing used never have I ever
@zhanna.message_handler(commands=["clear"])
def clear(message):
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)
    # getting data
    data = readData(message.from_user.id)
    # clearing history of never have i ever
    data["never_have_I_ever"].clear()
    # saving changes
    writeData(message, data)
    # replying to user
    zhanna.reply_to(message, "Я удалила историю игры")

# zhanna replyies to text
@zhanna.message_handler(content_types=["text"])
def main(message):
    # checks if user exist in data base 
    if not userExist(message.from_user.id):
        newUser(message)
    # check for chat and user data base
    if message.chat.type != "private":
        if not userExist(message.chat.id):
            newChat(message)
        userInChat(message)

    # getting answer
    answer = getAnswer(message)
    # if answer is not None then zhanna replyies to user
    if answer != None:
        zhanna.reply_to(message, "%s" %answer)
    # console output for administration
    consoleOutput(message, answer)

# bot pooling 
zhanna.polling(none_stop=True)