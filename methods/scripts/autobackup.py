import os
import datetime

day = datetime.datetime.now().day
if int(day)%7==0:
    os.system(f"zip -r /home/supperdoggy/backups/zhannabot_{str(datetime.date.today())} /home/supperdoggy/zhannabot")