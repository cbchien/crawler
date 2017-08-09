# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:43:18 2017

@author: user
"""
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

results = []

urls = ["https://www.machinio.com/excavators.json?page=1&format=json",
       "https://www.machinio.com/backhoe-loaders.json?page=1&format=json",
       "https://www.machinio.com/dozers.json?page=1&format=json",
       "https://www.machinio.com/crawler-loaders.json?page=1&format=json",
       "https://www.machinio.com/motor-graders.json?page=1&format=json"]
'''
urls=["https://www.machinio.com/hanomag/dozers.json?page=1"]
'''
def parseOnePage(urlTarget):
    '''
    print(urlTarget)
    '''
    raw = requests.get(urlTarget)
    rawOutput = raw.json()
    soup = BeautifulSoup(rawOutput["html"], "lxml")
    allItem = soup.find_all("li", {"class":"offer-listing"})
    category = urlTarget.replace("https://www.machinio.com/","").split(".")[0]
    print(len(allItem))
    try:
        nextUrl = "https://www.machinio.com" + rawOutput["next_page_data_url"] +"&format=json"
    except:
        nextUrl = ""
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
    try:
        parseOnePage(nextUrl)
    except Exception as e:
        print(e)


for url in urls:
    parseOnePage(url)
        
df = pd.DataFrame(results)

df.to_csv("machinio.csv", sep=',', encoding='utf-8')