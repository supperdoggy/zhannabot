from constants.constants import APIAITOKEN
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
                    "меня все заебало", "ты не итнересный", "подпишись на @rarezhanna, потом поговорим", 'я тебя не понимаю', 'я не научилась распознавать эту фразу', 'ты втираешь мне какую то дичь', 'что ты только что сказал?', 'давай сделаем вид что я поняла это сообщение', 'ты клоун', 'с тобой не интересно разговаривать', 'я не люблю когда мне говорят то что я не понимаю', 'ты сказал какую то чушь', 'я только робот, не могу поддержать этот разговор', 'иногда мне сложно понимат что ты пишешь', 'давай ты подпишешься на @rarezhanna, а потом продолжим разговор']
    return random.choice(possibleAnswers)

def answerCheck(answer):
    return answer if answer else IDontUnderstand()