from constants import APIAITOKEN
import apiai, json
import random

def getApiAiAnswer(message):
    request = apiai.ApiAI(APIAITOKEN).text_request()
    request.lang = "ru"
    request.session_id = "zhanna"
    request.query = message.text
    responseJson = json.loads(request.getresponse().read().decode("utf-8"))
    answer = responseJson["result"]["fulfillment"]["speech"]
    return answer

def IDontUnderstand():
    possibleAnswers = ["хочу спать", "хочу умереть", "дайте мне поспать", "как же хочется сдохнуть",
                    "меня все заебало", "ты не итнересный", "подпишись на @rarezhanna, потом поговорим"]
    return random.choice(possibleAnswers)

def answerCheck(answer):
    return answer if answer else IDontUnderstand()