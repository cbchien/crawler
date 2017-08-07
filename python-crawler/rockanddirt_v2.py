# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 11:42:36 2017

@author: cbchien
"""
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

results = []

mainCategoryUrl = {1048:"http://www.rockanddirt.com/equipment-for-sale/backhoes",
                   1040:"http://www.rockanddirt.com/equipment-for-sale/excavators",
                   1206:"http://www.rockanddirt.com/equipment-for-sale/excavators-mini",
                   1083:"http://www.rockanddirt.com/equipment-for-sale/excavators-wheel",
                   1173:"http://www.rockanddirt.com/equipment-for-sale/forklifts-telehandler",
                   1036:"http://www.rockanddirt.com/equipment-for-sale/forklifts-mast",
                   1057:"http://www.rockanddirt.com/equipment-for-sale/motor-graders",
                   1026:"http://www.rockanddirt.com/equipment-for-sale/crawler-loaders"}

indexs = [1048,1040,1206,1083,1173,1036,1057,1026]
maxads = 75

for index in indexs:
    startNum = 1
    firstweburl = "http://www.rockanddirt.com/search?&db=equipdb&catnum="+str(index)+"&maxads="+str(maxads)+"&zip=&start="+str(startNum)+"&method=search"
    print(firstweburl)
    firstpage = requests.get(firstweburl)
    soup = BeautifulSoup(firstpage.text, 'html.parser')
    maxNum = soup.find("div", {"class":"search_options"}).find("strong").text.split(" ")[2]

    while (startNum+75)<int(maxNum):
        startNum += maxads
        weburl = "http://www.rockanddirt.com/search?&db=equipdb&catnum="+str(index)+"&maxads="+str(maxads)+"&zip=&start="+str(startNum)+"&method=search"
        print(weburl)
        resultItems = soup.find_all("div", {"id":"result"}, True)
        
        for item in range(0, len(resultItems)):
            name = re.sub('[\n\r]', '',resultItems[item].find("li", {"class":"main"}).text)
            location = re.sub('[\n\r]', '', resultItems[item].find("li", {"class":"location"}).text)
            price = re.sub('[\n\r]', '', resultItems[item].find("li", {"class":"price"}).text)
            url = resultItems[item].find("li", {"class":"main"}).find("a")['href']
            
            try:
                odom = resultItems[item].find("li", {"class":"odom"}).text.replace("Hrs:","")
            except:
                odom = "N/A"
            
            try:
                description = re.sub('[\n\r]', '', resultItems[item].find("span", {"class":"descrip"}).text)
            except:
                description = "N/A"
            
            try:
                contact = re.sub('[\n\r]', '', resultItems[item].find("span", {"class":"contact"}).text)
            except:
                contact = "N/A"    
         
            results.append({
                    'name':name,
                    'hour':odom,
                    'price':price,
                    'category':mainCategoryUrl[index].split('/')[4],
                    'year':name.lstrip().split(" ")[0],
                    'location':location,
                    'contact':contact,
                    'url':url
                    })

df = pd.DataFrame(results)

df.to_csv("rockanddirt.csv", sep=',', encoding='utf-8')
