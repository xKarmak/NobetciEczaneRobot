# https://huzunluartemis.github.io/NobetciEczaneRobot/

from config import Config

def AuthUserCheck(message):
    if 0 in Config.AUTH_IDS: return True
    elif message.from_user.id in Config.AUTH_IDS: return True
    elif message.from_user.id == Config.OWNER_ID: return True
    elif message.chat.id in Config.AUTH_IDS: return True
    else: return False
