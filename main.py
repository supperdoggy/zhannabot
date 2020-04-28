import telebot
import random
from data import *
import os
import datetime
from constants import TOKEN
from methods import *
import apiai, json

# TODO: more punk

# zhanna = bot
zhanna = telebot.TeleBot(TOKEN)
@zhanna.message_handler(commands=["start"])
def greetings(message):
    # check for chat and user data base
    userDataBase(message)
    # getting greetings message
    answer = start(message.from_user.id)
    # zhanna replies to message
    zhannaReplies(zhanna, message, answer)
    # console output for administration
    consoleOutput(message, answer)

# command for getting personal fortune cookie
@zhanna.message_handler(commands=["fortune"])
def fortune(message):
    # check for chat and user data base
    userDataBase(message)
    # getting fortune cookie for user
    answer = getFortuneCookie(message)
    # zhanna answering
    zhannaReplies(zhanna, message, answer)
    # edditing the last time played
    editLastTimePlayed(message)
    # console output for administration
    consoleOutput(message, answer)

# antipara command
@zhanna.message_handler(commands=["antipara"])
def antipara(message):
    # check for chat and user data base
    userDataBase(message)
    # getting antipara
    answer = getAntipara(message)
    # answer is not None than zhanna answer to the command
    if answer:
        zhanna.reply_to(message, "%s"%answer)
    else:
        zhanna.reply_to(message, "Это работает только в публичных чатах!")
    # console output for administration
    consoleOutput(message, answer)

# TODO: refactor it 
@zhanna.message_handler(commands=["corona"])
def corona(message):
    # check for chat and user data base
    userDataBase(message)
    answer = getCorona(message)
    # zhanna replies to user with answer
    zhannaReplies(zhanna, message, answer)
    # console output for administration
    consoleOutput(message, answer)
    
# command for getting cheer tost
@zhanna.message_handler(commands=["tost"])
def tost(message):
    # check for chat and user data base
    userDataBase(message)
    # getting random tost as an answer for user
    answer = getTostAnswer()
    # replying to user
    zhannaReplies(zhanna, message, answer)
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
    zhannaReplies(zhanna, message, answer)
    # console output for administration
    consoleOutput(message, answer)

# command for getting random drink
@zhanna.message_handler(commands=["somilye"])
def somilye(message):
    # check for chat and user data base
    userDataBase(message)
    # getting random drink for user
    answer = getAlcohol(message.from_user.id)
    # replying to user
    zhannaReplies(zhanna, message, answer)
    # console output for administration
    consoleOutput(message, answer)

# never have i ever command
@zhanna.message_handler(commands=["neverhaveiever"])
def neverhaveiever(message):
    # check for chat and user data base
    userDataBase(message)
    # getting random neverHaveIEver statement
    answer = getNHIEAnswer(message)
    # replying to user
    zhannaReplies(zhanna, message, answer)
    # appending new statement into the history
    appendNeverEver(message, answer)
    # console output for administration
    consoleOutput(message, answer)

# hidden command for clearing used never have I ever
@zhanna.message_handler(commands=["clear"])
def clear(message):
    # check for chat and user data base
    userDataBase(message)
    # getting data
    data = readData(message.from_user.id)
    # clearing history of never have i ever
    data["never_have_I_ever"].clear()
    # saving changes
    writeData(message, data)
    # replying to user
    zhanna.reply_to(message, "Я удалила историю игры")

@zhanna.message_handler(commands=["flower"])
def growFlower(message):
    # check for chat and user data base
    userDataBase(message)
    # getting answer
    answer = flower(message)
    # zhanna replies
    zhannaReplies(zhanna, message, answer)
    # consnole output for administration
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["myflowers"])
def myFlowers(message):
    # check for chat and user data base
    userDataBase(message)
    # getting answer
    answer = getFlowers(message) + "\n" + getFlowerTypes(message)
    # zhanna replies
    zhannaReplies(zhanna, message, answer)
    # console output for administration
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["flowertop"])
def topFlowers(message):
    # check for chat and user data base
    userDataBase(message)    
    # getting answer
    answer = getTopFlowers(message)
    # zhanna replies to user
    zhannaReplies(zhanna, message, answer)
    # console output for administration
    consoleOutput(message, answer)

@zhanna.message_handler(commands=["giveoneflower"])
def giveOneFLower(message):
    # check for chat and user data base
    userDataBase(message) 
    # getting answer
    answer = sendFlower(message)
    # zhanna replies to user
    zhannaReplies(zhanna, message, answer)
    # console output for administration
    consoleOutput(message, answer)

# zhanna replyies to text
@zhanna.message_handler(content_types=["text"])
def main(message):
    try:
        # check for chat and user data base
        userDataBase(message)
        # getting answer
        answer = getAnswer(message)
        # zhanna replies to user
        zhannaReplies(zhanna, message, answer)
        # console output for administration
        consoleOutput(message, answer)
    except:
        pass

# bot pooling 
zhanna.polling(none_stop=False, interval=1, timeout=1)
