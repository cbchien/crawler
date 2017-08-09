# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:43:18 2017

@author: user
"""
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import math

results = []

urls = [
       "https://www.machinio.com/backhoe-loaders/united-states.json?page=1&format=json",
       "https://www.machinio.com/dozers/united-states.json?page=1&format=json",
       "https://www.machinio.com/crawler-loaders/united-states.json?page=1&format=json",
       "https://www.machinio.com/motor-graders/united-states.json?page=1&format=json"]
'''
urls=["https://www.machinio.com/excavators/united-states.json?page=1&format=json"]
'''
def parseOnePage(urlTarget):
    raw = requests.get(urlTarget)
    rawOutput = raw.json()
    soup = BeautifulSoup(rawOutput["html"], "lxml")
    allItem = soup.find_all("li", {"class":"offer-listing"})
    print("item count:",len(allItem),urlTarget)
    category = urlTarget.replace("https://www.machinio.com/","").split(".")[0]
    for item in range(0, len(allItem)):
        title = allItem[item].find("h4",{"class":"offer-listing__title"}).text
        price = allItem[item].find("div",{"class":"price"}).text
        url = allItem[item].find("a",{"class":"ellipsis"})['href']
        try:
            manufacturer = allItem[item].find("span",{"itemprop":"manufacturer"}).text 
        except:
            manufacturer = "N/A"
        try:
            location = allItem[item].find("div",{"class":"location"}).text
        except:
            location = "N/A"
        try:
            description = re.sub('[\n\r]', '', allItem[item].find("p",{"itemprop":"description"}).text)
        except:
            description = "N/A"
        try:
            hour = allItem[item].find("p",{"class":"offer-listing__description"}).previousSibling.text.split(" ")[1]
        except:
            hour = "N/A"
            
        results.append({
                    'name':title,
                    'category':category,
                    'hour':hour,
                    'price':price,
                    'year':re.sub('[a-zA-Z]','',title.split(" ")[0]),
                    'manufacturer':manufacturer,
                    'description':description,
                    'location':location,
                    'url':url
                    })

for url in urls:
    a = requests.get(url.split(".json")[0])
    soup = BeautifulSoup(a.text, "lxml")
    maxNum = int(soup.find("div",{"role":"banner"}).text.split(" ")[0])
    requestTime = math.ceil(maxNum / 10)
    temp = re.sub('[\d]', '#', url)
    startNum = math.ceil(int(requestTime+1)/3)*2
    endNum = int(requestTime+1)
    '''
    int(requestTime+2)'''
    for i in range(int(startNum),int(endNum)):
        thisUrl = temp.split("#")[0]+str(i)+temp.split("#")[1]
        try:
            parseOnePage(thisUrl)
        except:
            pass
df = pd.DataFrame(results)
df.to_csv("machinio_p3.csv", sep=',', encoding='utf-8')