# https://huzunluartemis.github.io/NobetciEczaneRobot/

import os
import time
from pyrogram.types.messages_and_media.message import Message
from config import Config, LOGGER
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.eczaneScrapers import eczaneCollectApi, eczaneEczaIo, eczaneEczanelerGenTr, \
    eczaneEczaneleriNet, eczaneEczaneleriOrg, eczaneHastanemyanimdaCom, eczaneNosyApi, eczaneTrNobetcieczaneCom
from helper_funcs.force_sub import ForceSub
from pyrogram import Client, filters

quee = []

def runScraper(il, ilce):
    if Config.USING_API.lower() == "collectapi":
        return eczaneCollectApi(il,ilce)
    elif Config.USING_API.lower() == "nosyapi":
        return eczaneNosyApi(il,ilce)
    elif Config.USING_API.lower() == "eczaneleriorg":
        return eczaneEczaneleriOrg(il,ilce)
    elif Config.USING_API.lower() == "eczanelergentr":
        return eczaneEczanelerGenTr(il,ilce)
    elif Config.USING_API.lower() == "hastanemyanimdacom":
        return eczaneHastanemyanimdaCom(il,ilce)
    elif Config.USING_API.lower() == "eczanelerinet":
        return eczaneEczaneleriNet(il,ilce)
    elif Config.USING_API.lower() == "trnobetcieczanecom":
        return eczaneTrNobetcieczaneCom(il,ilce)
    elif Config.USING_API.lower() == "eczaio":
        return eczaneEczaIo(il,ilce)
    else:
        LOGGER.error("Uygun api seçilmedi, bot kapatılıyor. Lütfen okuyun: https://huzunluartemis.github.io/NobetciEczaneRobot/")
        return exit(1)

def run_task(gelen: Message, duzenlenecek: Message):
    try:
        # custom filename
        link = gelen.text
        il, ilce =  link.split(" ")
        x = runScraper(il, ilce)
        if not x:
            duzenlenecek.edit_text("Bilgiler alınamadı. Lütfen bot sahibine bildiriniz.")
        else:
            if Config.CHANNEL_OR_CONTACT:
                x += f"\n\n{Config.CHANNEL_OR_CONTACT}"
            if len(x) > 3000:
                with open('eczaneler.txt', 'w') as file: file.write(x)
                with open('eczaneler.txt', 'rb') as doc:
                    gelen.reply_document(
                        document=doc,
                        caption="Çok uzundu. Bu dosyayı açıp okuyabilirsin.")
                duzenlenecek.delete()
                if os.path.isfile('eczaneler.txt'): os.remove('eczaneler.txt')
            else:
                duzenlenecek.edit_text(x, disable_web_page_preview=True)
    except Exception as e:
        duzenlenecek.edit_text("Cannot download. Try again later.")
        LOGGER.exception(e)
    on_task_complete()

def on_task_complete():
    if len(quee) > 0:
        del quee[0]
    if len(quee) > 0:
        time.sleep(10)
        run_task(quee[0][0], quee[0][1])

@Client.on_message(filters.command(["help", "yardım", "yardim", "start", "h", "y"]))
def welcome(_, message: Message):
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    text=f"""Hi / Merhaba {message.from_user.mention}.

🇹🇷 Ben basit bir nöbetçi eczane botuyum.
Bulunduğunuz bölgedekileri listelemek için Şehir [boşluk] ilçe olarak girin.
Sıra önemli. önce il sonra ilçe yazmalısın.

🇬🇧 I'm a simple on-duty pharmacy bot.
To list duty pharmacies in your area Enter the city   [space] district.
The order matters. You should write the city first and then the county.

💜 Örnekler / Examples:

Çanakkale Merkez
İzmir Aliağa
Samsun Alaçam
Konya Çumra

[💚](https://huzunluartemis.github.io/NobetciEczaneRobot/) Kullanlan API: {Config.USING_API}"""
    if Config.CHANNEL_OR_CONTACT: text += f"\n🔥 {Config.CHANNEL_OR_CONTACT}"
    message.reply_text(text=text,disable_web_page_preview=True)

@Client.on_message(filters.text)
def handler(_, message: Message):
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    # add to quee
    try:
        if len(message.text.split(" ")) == 2:
            duz = message.reply_text(f"✅ Your Turn / Sıranız: {len(quee)+1}\nWait / Bekleyin.", quote=True)
            quee.append([message, duz])
            if len(quee) == 1: run_task(message, duz)
    except:
        tex = """🇹🇷 Şehir ya da ilçeyi yanlış girdiniz.
Şehir [boşluk] ilçe olarak girin.

✅ Doğru örnekler:
Çanakkale Merkez
İzmir Aliağa

❌ Yanlış örnekler:
G antep araban
K maraş elbistan
G.antep nizip

🇬🇧 You entered the city or town incorrectly.
Enter the city   [space] district.

✅ Examples:
Samsun Alaçam
Konya Çumra

❌ Wrong examples:
Ş urfa halfeti
Şanlı urfa akçakale
Ş.urfa Suruç"""
        message.reply_text(tex, quote=True)
