# https://huzunluartemis.github.io/NobetciEczaneRobot/

import os
from zipfile import ZipFile
import requests
from webdriver_manager.chrome import ChromeDriverManager
from config import LOGGER
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def karakter_cevir(metin):
    tr_chars = {
    "ç": "c",
    "Ç": "c",
    "ğ": "g",
    "Ğ": "g",
    "ı": "i",
    "İ": "i",
    "I": "i",
    "ö": "o",
    "Ö": "o",
    "ş": "s",
    "Ş": "s",
    "ü": "u",
    "Ü": "u",
    }
    for karakter in tr_chars:
        metin = metin.replace(karakter, tr_chars[karakter])
    return metin

def removespace(str, withnewline=True):
    if not str: return None
    if len(str) < 1: return None
    str = str.replace("\n", "")
    str = str.replace("  ", "", 50)
    str = str.strip()
    if withnewline: return f"{str}\n"
    else: return str

def getUblockPath():
    ublockMainPath = os.path.join(os.getcwd(), 'ublock')
    ublockZipPath = os.path.join(os.getcwd(), 'ublock', 'ublock.zip')
    ublockFinalPath = os.path.join(os.getcwd(), 'ublock', 'uBlock0.chromium')
    if os.path.isfile(ublockZipPath): return ublockFinalPath
    # ublock alınıyor
    try:
        LOGGER.info("installing ublock...")
        ublockurl = 'https://github.com/gorhill/uBlock/releases/download/1.43.0/uBlock0_1.43.0.chromium.zip'
        r = requests.get(ublockurl, allow_redirects=True)
        if not os.path.isdir('ublock'): os.mkdir('ublock')
        open(ublockZipPath, 'wb').write(r.content)
        # çıkar
        with ZipFile(ublockZipPath, 'r') as zipObj: zipObj.extractall(path=ublockMainPath)
        return ublockFinalPath
    except Exception as e:
        LOGGER.error("failed install ublock.")
        return None

def initAllThings():
    LOGGER.info("initilaizing required things...")
    try:
        chrome_options = Options()
        chrome_options.add_argument(f'load-extension={getUblockPath()}')
        chrome_options.add_argument("--lang=tr-TR")
        chrome_options.add_argument("--headless")
        chrome_options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.close()
    except Exception as e:
        LOGGER.exception(e)
        LOGGER.error("Selenium will not work. Build failed.")
    getUblockPath()
    LOGGER.info("initilaizing required things... Done.")
