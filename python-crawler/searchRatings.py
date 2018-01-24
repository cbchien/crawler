# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:49:17 2017

@author: user
"""

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

results = []


entry = ["(晶華酒店)上庭酒廊","ONE9Bar","HangOutCocktailBar","台日交流Cafe&BarKiseki","Mudan","HeroBar,Taipei","XiaoxiongCunCafe","EZBar","笨嗽音吶BSINDarts&Bar","酒肆西門XimenBeerBar","SALUD","AQCava","ansleepcafe+bar","ROOMJ","Via24Bar","Prostbar","Midway","GoldfishBar","BarTurningPoint","Husband餐酒館「HusbandLoungeBar」","寓SALON&BAR","PATINALounge","QueenCoffee【慢。輕食。鬆餅】WaffleCoffeeShop","BARNiNE","THEgarden花園小酒館","嘉麗寶會館","WTaipeiWET池畔酒吧","MattBar","備長炭CarbonBar&Bistro","ansleep","FiFi茶酒沙龍WBar","TipsyTaipeiCafe&BAR微醺台北","7thJapaneseBar","KhakiCaféBar","ABar","OxygenObar&Cafe","BochibochiBar","HuntTaipei","ㄧ號倉庫炭火串燒Bar","酒窖子Winebar&Wineshop","CaféDalida","HOKY'sSpiritBar","楓木餐酒館MapleBar","ZOOBar&Bistro","BarM","焼酎Bar五右衛門","TheStandingRoom","BacchusLoungeBar","RelaxJazzPub","M.O.Bar","小公園PiccoloParcoCaffeeBar","MirrorLounge","JamesJoyceIrishBar","Vaultcafe&Bar","亂調","FRANKTaipei","mud酒吧","Crafted-Beer&Co.","Nep.LoungeBar","TheDaftHouse","Nami串燒bar","MotownTaipei","Cellar","NoxTaipei","馬可波羅酒廊（MarcoPoloLounge）-香格里拉台北遠東國際大飯店","SantéLounge&Bar","DaBar-Relax/Social/Mingle","MONOMONO","乾杯Bar安和店","GreenDoor","HANKO60","Barry&Gabriela's小酒趴","石洞PUB(MyPlace)","ProzacBalcony百憂解陽台","二升五合燒肉Bar","BAR小谷","Ounce","Beau","LeZinc洛Café&Bar","SoShowBar&Restaurant","Mod二店","CommanderD","KushiBar","摩得餐坊","85LOUNGE","EastEndBar","Driftwood西門町","TheSpeakeasyBar","MayBEMusicBar","BOBWUNDAYE","MVSAspanishrestaurant&bar","SapphoLiveJazz","AlchemySpeakeasyBarTaipei","Larriere-cour","串場KushiBar(忠孝店)","Placebo安慰劑小酒館","Digout","ABVBar&Kitchen加勒比海餐酒館-精釀啤酒餐廳","RoxyRocker","WOOBAR","1001NightsTaipei","Triangle","榕RON","INDULGEBistro(實驗創新餐酒館)","Barcode","TrioOriginal","PeacockBistro","MikkellerTaipei米凱樂啤酒吧","Ticklemyfantasy","FourplayCuisine","EZ5LiveHouse音樂餐廳","TheWallLiveHouse公館","JAPJAPBIKINI","BrownSugarLive&Restaurant","INHOUSE","Kanpai","Revolver","WooTaipei窩台北","PSTAPAS西班牙餐酒館","BrassMonkeyFuxing","ONTAP","MitsuiJapaneseCuisine","DozoIzakayaBar"]
'''
entry = ["(晶華酒店)上庭酒廊","ONE9Bar","HangOutCocktailBar"]
'''
for i in range(0, len(entry)):
    url = 'http://www.google.com/search?q='+entry[i]
    print('current entry',entry[i])
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    '''add entry with no rating results'''
    if len(soup.findAll('div',{'class':'slp'})) == 0:
        results.append({
                'name': entry[i],
                'vote': ''
                })
    
    '''find all g class to return url'''
    match = soup.findAll('div',{'class':'g'})

    for j in range(0,len(match)):
        if match[j].find('div',{'class':'slp'}) is None: 
            pass
        elif "facebook" in match[j].find('cite').text:
            vote = re.sub('[\xa0]', '',match[j].find('div',{'class':'slp'}).text)      
            url = match[j].find('cite').text
            results.append({
                    'name': entry[i],
                    'vote': vote,
                    'url': url
                    })
        else:
            results.append({
                'name': entry[i],
                'vote': ''
            })
df = pd.DataFrame(results)
df.to_csv("searchrating.csv", sep=',', encoding='utf-8')