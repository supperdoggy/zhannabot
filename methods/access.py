from constants.constants import BANNED_USERS
# check for userId
def isBanned(id):
    return True if id in BANNED_USERS else False