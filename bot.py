# https://huzunluartemis.github.io/NobetciEczaneRobot/

from config import LOGGER, Config
from pyrogram import idle
import pyrogram

from helper_funcs.eczaneFuncs import initAllThings

if __name__ == '__main__':
    # init pyrogram client
    plugins = dict(root = 'plugins')
    app = pyrogram.Client("NobetciEczaneRobot", bot_token = Config.BOT_TOKEN,
        api_id = Config.APP_ID, api_hash = Config.API_HASH, plugins = plugins)
    app.start()
    initAllThings()
    
    LOGGER.info(app.get_me())
    LOGGER.info(msg="Bot Started.")
    try: app.send_message(Config.OWNER_ID, "Bot Started.")
    except: pass
    idle()
    LOGGER.info(msg="Bot Stopped.")
    try: app.send_message(Config.OWNER_ID, "Bot Stopped.")
    except: pass
