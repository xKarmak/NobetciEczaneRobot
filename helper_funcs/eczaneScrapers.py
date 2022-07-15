# https://huzunluartemis.github.io/NobetciEczaneRobot/

import urllib.parse
from bs4 import BeautifulSoup
import bs4
import requests
from config import LOGGER, Config
from helper_funcs.eczaneFuncs import getUblockPath, karakter_cevir, removespace
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import http.client
import json

def eczaneCollectApi(il, ilce): # ok
        main_api="https://api.collectapi.com/health/dutyPharmacy?"
        url = main_api + urllib.parse.urlencode({"ilce": ilce, "il": il})
        headers = {
            'content-type': "application/json",
            'authorization': f"apikey {Config.API_KEY}"
            }
        veri = (requests.post(url,headers=headers)).json()
        if veri['success']:
            ret = list()
            for her in veri["result"]:
                stro = ""
                if her['name']: stro += her['name']
                #if her['dist']: stro += f"\nİlçe: {str(her['dist'])}"
                if her['address']: stro += f"\n{her['address']}"
                if her['phone']: stro += f"\n{her['phone']}"
                if her['loc']: stro += f"\nhttps://maps.google.com/maps?q={str(her['loc'])}" # &hl=es&z=14
                ret.append(stro)
            return "\n\n".join(ret)
        else:
            return None

def eczaneNosyApi(il, ilce): # ok
    il = karakter_cevir(il)
    ilce = karakter_cevir(ilce)
    conn = http.client.HTTPSConnection("www.nosyapi.com")
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {Config.API_KEY}'
    }
    conn.request("GET", f"/apiv2/pharmacy?city={il}&county={ilce}", 'payload', headers)
    res = conn.getresponse()
    data = res.read().decode('utf8')
    data = json.loads(data)
    #
    
    if data['status']:
        veriler = data['data']
        ret = list()
        for her in veriler:
            stro = ""
            if her['EczaneAdi']: stro += her['EczaneAdi']
            #if her['dist']: stro += f"\nİlçe: {str(her['dist'])}"
            if her['Adresi']: stro += f"\n{her['Adresi']}"
            if her['YolTarifi']: stro += f"\n{her['YolTarifi']}"
            if her['Telefon']: stro += f"\n{her['Telefon']}"
            if her['Telefon2']: stro += f"\n{her['Telefon2']}"
            if her['latitude'] and her['longitude']:
                lat = her['latitude']
                lng = her['longitude']
                stro += f"\nhttps://www.google.com/maps/search/?api=1&query={lat},{lng}"
            ret.append(stro)
        return "\n\n".join(ret)
    else:
        return None

def eczaneEczaneleriOrg(il, ilce):
    il = karakter_cevir(il)
    ilce = karakter_cevir(ilce)
    url = f"https://{il}.eczaneleri.org/{ilce}/nobetci-eczaneler.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if not response.status_code == 200:
        return print("Bağlantı Hatası")
    liste = BeautifulSoup(response.content, "html.parser")
    liste = liste.find("div", attrs={"class": "pane-wrapper"})
    liste = liste.find("div", attrs={"class": "active"})
    nezamanadek = liste.find("div", attrs={"class": "alert alert-warning"}).text
    nezamanadek = removespace(nezamanadek, withnewline=False)
    liste = liste.find_all("div", attrs={"class": "media-body"})
    tumu = [nezamanadek]
    for col in liste:
        her = ""
        adi = col.h4.contents[0]
        # info kutusu 1
        infokutu1 = col.find("span", attrs={"class": "label-default"})
        if infokutu1: infokutu1 = col.find("span", attrs={"class": "label-default"}).text
        else: infokutu1 = None
        # info kutusu 2
        infokutu2 = col.find("span", attrs={"class": "label-info"})
        if infokutu2: infokutu2 = col.find("span", attrs={"class": "label-info"}).text
        else: infokutu2 = None
        # 
        if removespace(adi): her += removespace(adi)
        if removespace(col.text): her += removespace(col.text)
        if removespace(infokutu1): her += removespace(infokutu1)
        # if removespace(infokutu2): her += removespace(infokutu2) ilçeyi veriyor gereksiz
        # checking again for tel number
        fortel = col.find("a")['href']
        url = f"https://{il}.eczaneleri.org/{fortel}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if not response.status_code == 200:
            return print("Bağlantı Hatası")
        fortel = BeautifulSoup(response.content, "html.parser")
        # adres falan
        telefon = fortel.find("div", attrs={"class": "pull-left"})
        if telefon:
            telefon = fortel.find("div", attrs={"class": "pull-left"}).contents[0].strip()
            telefon = telefon.replace("Telefon : ", "Telefon: ") # yazım hatasını düzelt
        else: telefon = None
        #
        if removespace(telefon): her += removespace(telefon)
        konum = fortel.find("button", attrs={"class": "btn btn-block btn-success btn-sm"})
        if konum:
            lat = konum['lat']
            lng = konum['lng']
            gmapsurl = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
            her += removespace(gmapsurl, withnewline=False)
        tumu.append(her)
    return "\n\n".join(tumu)

def eczaneEczanelerGenTr(il, ilce):
    # edited version: https://github.com/keyiflerolsun/KekikSpatula/blob/main/KekikSpatula/nobetciEczane.py
    il = karakter_cevir(il)
    ilce = karakter_cevir(ilce)
    url     = f"https://www.eczaneler.gen.tr/nobetci-{il}-{ilce}"
    istek   = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})
    corba = BeautifulSoup(istek.content, "lxml")
    bugun = corba.find('div', id='nav-bugun')
    if not bugun: return None
    tumu = []
    for bak in bugun.findAll('tr')[1:]:
        bu = ""
        ad = bak.find('span', class_='isim').text if bak.find('span', class_='isim') else None
        mah = (None if bak.find('div', class_='my-2') is None else bak.find('div', class_='my-2').text)
        adres = bak.find('div', class_='col-lg-6').text if bak.find('div', class_='col-lg-6') else None
        tarif = (None if bak.find('span', class_='text-secondary font-italic') is None else bak.find('span', class_='text-secondary font-italic').text)
        telf = bak.find('div', class_='col-lg-3 py-lg-2').text if bak.find('div', class_='col-lg-3 py-lg-2') else None
        if ad: bu += removespace(ad)
        if mah: bu += removespace(mah)
        if adres: bu += removespace(adres)
        if tarif: bu += removespace(tarif)
        if telf: bu += removespace(telf, withnewline=False)
        tumu.append(bu)
    return "\n\n".join(tumu)

def eczaneHastanemyanimdaCom(il, ilce):
    il = karakter_cevir(il)
    ilce = karakter_cevir(ilce)
    url = f"https://www.hastanemyanimda.com/nobetci-eczane/{il}/{ilce}"
    istek   = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})
    corba = BeautifulSoup(istek.content, "lxml")
    bugun = corba.find_all("div", attrs={"class": "doctor-widget"})
    if not bugun: return None
    tumu = []
    for bak in bugun:
        bu = ""
        ad = bak.find('h2', class_='doc-name mb-2').text if bak.find('h2', class_='doc-name mb-2') else None
        telf = bak.find('div', class_='clini-infos pt-3').find("a").text
        adres = bak.find('p', class_='doc-location mb-2 text-ellipse').text
        gharita = bak.find('a', class_='apt-btn')['href']
        ydeskharita = bak.find('a', class_='view-pro-btn')['href']
        if ad: bu += removespace(ad)
        if telf: bu += removespace(telf)
        if adres: bu += removespace(adres)
        if gharita: bu += removespace(gharita)
        if ydeskharita: bu += removespace(ydeskharita, withnewline=False)
        tumu.append(bu)
    return "\n\n".join(tumu)

def eczaneEczaneleriNet(il, ilce):
    il = karakter_cevir(il)
    ilce = karakter_cevir(ilce)
    url = f"https://{il}.eczaneleri.net/{ilce}-nobetci-eczaneleri"
    istek   = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})
    corba = BeautifulSoup(istek.content, "lxml")
    bugun = corba.find_all("div", attrs={"class": "pro-content"})
    if not bugun: return None
    tumu = []
    for bak in bugun:
        bu = ""
        ad = bak.find('h3', class_='h3').find('span').text if bak.find('h3', class_='h3').find('span') else None
        telf = bak.find('i', class_='fas fa-phone')
        if telf: telf = telf.parent.contents[3].text if telf.parent.contents[3] else None
        adres = bak.find('address', class_='d-inline m-0').text if bak.find('address', class_='d-inline m-0') else None
        if ad: bu += removespace(ad)
        if telf: bu += removespace(telf)
        if adres: bu += removespace(adres,withnewline=False)
        tumu.append(bu)
    return "\n\n".join(tumu)

def eczaneTrNobetcieczaneCom(il, ilce):
    il = karakter_cevir(il)
    ilce = karakter_cevir(ilce)
    url = f"https://www.trnobetcieczane.com/ilce/{il}-{ilce}-nobetci-eczaneler/"
    istek   = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})
    corba = BeautifulSoup(istek.content, "lxml")
    bugun = corba.find_all("div", attrs={"class": "eczanelistcontent"})
    if not bugun: return None
    tumu = []
    for bak in bugun:
        bu = ""
        ad = bak.find('a', class_='ta').text
        telf = bak.find('div', class_='eczanephone').find("a").text
        adres = bak.contents[1].text.replace("Adres", "")
        # tekrar git harita için
        haritalik = bak.find('a', class_='maps-link')['href']
        haritalik = f"https://www.trnobetcieczane.com/{haritalik}"
        istek2   = requests.get(haritalik, headers = {"User-Agent": "Mozilla/5.0"})
        corba2 = BeautifulSoup(istek2.content, "lxml")
        harita = corba2.find("a", attrs={"class": "gbutton"})['href']
        if ad: bu += removespace(ad)
        if telf: bu += removespace(telf)
        if adres: bu += removespace(adres)
        if harita: bu += removespace(harita,withnewline=False)
        tumu.append(bu)
    return "\n\n".join(tumu)

def eczaneEczaIo(il, ilce):
    il = karakter_cevir(il)
    ilce = karakter_cevir(ilce)
    url = f"https://ecza.io/{il}-{ilce}-nobetci-eczane"
    try:
        # selenyum ayarları
        chrome_options = Options()
        chrome_options.add_argument(f'load-extension={getUblockPath()}')
        chrome_options.add_argument("--lang=tr-TR")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.create_options()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        bugun:bs4.Tag = soup.find_all("div", attrs={"class": "section"})[0]
        bugun = bugun.find_all("div", attrs={"class": "pharmacy-card-item pharmacy-card-item--type-inline"})
        if not bugun: return None
        tumu = []
        for bak in bugun:
            bu = ""
            ad = bak.find("span", attrs={"class": "pharmacy-card-item__text pharmacy-card-item__text--pharmacy"})
            ad = ad.find("a", attrs={"class": "we"}).text
            telf = bak.find("mark").text
            adres = bak.find_all("div", attrs={"class": "pharmacy-card-item__col"})[2]
            adres = adres.find("span", attrs={"class": "pharmacy-card-item__text"}).text
            
            if ad: bu += removespace(ad)
            if telf: bu += removespace(telf)
            if adres: bu += removespace(adres, withnewline=False)
            tumu.append(bu)
        return "\n\n".join(tumu)
    except Exception as e:
        LOGGER.exception(e)
        return None
