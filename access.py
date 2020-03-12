from constants import BANNED_USERS
# check for userId
def idCheck(id):
    return True if id not in BANNED_USERS else False