# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:41:25 2017

@author: cbchien
"""

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

results = []

urls = ["http://www.equipmenttrader.com/Construction-Equipment/Excavators-For-Sale/search-results?category=Excavators|2000206",
        "http://www.equipmenttrader.com/Construction-Equipment/Dozers-For-Sale/search-results?category=Dozers|2000202",
        "http://www.equipmenttrader.com/Construction-Equipment/Backhoes-For-Sale/search-results?category=Backhoes|2000200"]

for url in urls:
    firstpage = requests.get(url)
    soup = BeautifulSoup(firstpage.text, 'html.parser')
    maxPage = int(soup.find("span",{"id":"currentPagNum"}).nextSibling.split(" ")[2])
    listing = []
    
    for i in range(1,int((maxPage+1)/4*4)):
        currentUrl = url+"&page="+str(i)
        currentPage = requests.get(currentUrl)
        print(currentUrl)
        currentSoup = BeautifulSoup(currentPage.text, 'html.parser')
        
        for j in range(0,25):
            try:
                listing.append(currentSoup.findAll("div",{"class":"listing"})[j].find("a")["adid"])
            except:
                pass
            
    for k in range(0,len(listing)):
                detailUrl = "http://www.equipmenttrader.com/listing/-"+str(listing[k])+"?quickView=1"
                try:
                    detailPage = requests.get(detailUrl)
                except requests.exceptions.ConnectionError:
                    print("Connection refused",listing)
                print(detailUrl)
                detailSoup = BeautifulSoup(detailPage.text, 'html.parser')
                alltitle = detailSoup.findAll("span",{"class":"width40 bold"})
                alldescription = detailSoup.findAll("span",{"class":"width60"})
                specCount = len(alltitle)
                thisListing={}
                try:
                    location = re.sub('[\n]', '',detailSoup.find("div",{"class":"margin5-0 padding5-0 border-top1"}).text)
                except:
                    pass
                thisListing.update({"location": location})
                for h in range(0,specCount):
                    thisListing.update({
                            alltitle[h].text : alldescription[h].text
                            })
                results.append(thisListing)

df = pd.DataFrame(results)
df.to_csv("equipmenttrader_Excavators.csv", sep=',', encoding='utf-8')
        
        