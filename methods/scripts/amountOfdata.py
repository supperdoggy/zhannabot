from os import listdir
from constants.constants import *

def amountOfData():
    print("Amount of data:", len(listdir(FULL_PATH + f"{CHAT_DATA_PATH}/")))
    print("Amount of flower_data:", len(listdir(FULL_PATH + f"{FLOWER_DATA_PATH}/")))

if __name__ == "__main__":
    amountOfData()
     