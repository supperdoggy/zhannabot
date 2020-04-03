from os import listdir
from constants import FULL_PATH

def amountOfData():
    print("Amount of data:", len(listdir(FULL_PATH + "data/")))
    print("Amount of flower_data:", len(listdir(FULL_PATH + "flower_data/")))

if __name__ == "__main__":
    amountOfData()
     