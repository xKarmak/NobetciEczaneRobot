# https://huzunluartemis.github.io/NobetciEczaneRobot/

import logging
import os
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
botStartTime = time.time()

class Config:
    
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    APP_ID = int(os.environ.get('APP_ID', 1111111))
    API_HASH = os.environ.get('API_HASH', '')
    AUTH_IDS = [int(x) for x in os.environ.get("AUTH_IDS", "0").split()] # if open to everyone give 0
    OWNER_ID = int(os.environ.get('OWNER_ID', 0)) # give your owner id # if given 0 shell will not works
    FORCE_SUBSCRIBE_CHANNEL = os.environ.get('FORCE_SUBSCRIBE_CHANNEL','') # force subscribe channel link.
    CHANNEL_OR_CONTACT = os.environ.get('CHANNEL_OR_CONTACT', "HuzunluArtemis") # give your public channel or contact username
    CHANNEL_OR_CONTACT = f"@{CHANNEL_OR_CONTACT}"
    HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY', "")
    HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', "")
    USING_API  = os.environ.get('USING_API', "eczaneEczanelerGenTr")
    API_KEY = os.environ.get('API_KEY', "")

    # chromedriver paths
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', "/app/.chromedriver/bin/chromedriver")
    GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', "/app/.apt/usr/bin/google-chrome")

    if USING_API.lower() in ["eczanecollectapi", "nosyapi"] and len(API_KEY) < 5:
        LOGGER.error("API_KEY girin. Bot kapanıyor çünkü küstü.")
        exit(1)
    #customisations
    JOIN_CHANNEL_STR = os.environ.get('JOIN_CHANNEL_STR',
        "Merhaba / Hi {}\n\n" + \
        "🇬🇧 First subscribe my channel from button, try again.\n" + \
        "🇹🇷 Önce butondan kanala abone ol, tekrar dene.")
    YOU_ARE_BANNED_STR = os.environ.get('YOU_ARE_BANNED_STR',
        "🇬🇧 You are Banned to use me.\n🇹🇷 Banlanmışsın ezik.\n\nDestek / Support: {}")
    JOIN_BUTTON_STR = os.environ.get('JOIN_BUTTON_STR', "🇬🇧 Join / 🇹🇷 Katıl")
    
    # fixing vars
    if FORCE_SUBSCRIBE_CHANNEL == "" or FORCE_SUBSCRIBE_CHANNEL == " " or len(str(FORCE_SUBSCRIBE_CHANNEL)) == 0: FORCE_SUBSCRIBE_CHANNEL = None # bu satıra dokunmayın.
    if HEROKU_API_KEY  == "" or HEROKU_API_KEY == " " or len(HEROKU_API_KEY) == 0: HEROKU_API_KEY = None # bu satıra dokunmayın.
    if HEROKU_APP_NAME  == "" or HEROKU_APP_NAME == " " or len(HEROKU_APP_NAME) == 0: HEROKU_APP_NAME = None # bu satıra dokunmayın.
