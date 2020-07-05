import os
import re

def getFileList():
    LOGS_PATH = "logs/"
    files = os.listdir(LOGS_PATH)
    files.sort()
    uniqueUsers = []
    for f in files:
        with open(LOGS_PATH+f) as file:
            text = file.read()
            results = re.findall("Мне написал человек с юзернеймом: (.+)", text)
            for n in results:
                if n not in uniqueUsers:
                    uniqueUsers.append(n)

        print(f"{f} {len(uniqueUsers)} unique users")
        uniqueUsers = []

if __name__ == "__main__":
    getFileList()

