# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 09:47:36 2017

@author: user
"""

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import json  

results = []

url="https://jobbatical.com/jobs"

urls=[]

mainpage = requests.get(url)
soup = BeautifulSoup(mainpage.text, 'html.parser')
allPosting = soup.find_all("div", {"class":"jb-listing-card"})

for i in range(0,len(allPosting)):
    urls.append(allPosting[i].find("a")['href'].replace("u'","'"))

for j in range(0,len(allPosting)):
    print(j)
    jobUrl = "https://jobbatical.com"+urls[j]
    detailpage = requests.get(jobUrl)
    soup = BeautifulSoup(detailpage.text, 'html.parser')
    detailJson = json.loads(re.sub("[\n\r]","",soup.find("script", {"type":"application/ld+json"}).get_text()))
    try:
        results.append({
                "name": detailJson["title"],
                "datePosted": detailJson["datePosted"],
                "hiringOrganization": {
                	   "name": detailJson["hiringOrganization"]["legalName"],
                	   "location": {
                    "addressRegion": detailJson["hiringOrganization"]["location"]["address"]["addressRegion"],
                    "addressCountry": detailJson["hiringOrganization"]["location"]["address"]["addressCountry"]
                	}
                },
                "pictures": ["http://"],
                "description": detailJson["description"],
                "category": "Category.categorySchema",
                "icentiveCompensation": detailJson["incentiveCompensation"],
                "jobLocation": {
                	   "addressCity": detailJson["jobLocation"]["address"]["addressLocality"],
                    "addressRegion": detailJson["jobLocation"]["address"]["addressRegion"],
                    "addressCountry": detailJson["jobLocation"]["address"]["addressCountry"]
                },
                "employmentType": "full-time",
                "industry": detailJson["industry"],
                "responsibilities": detailJson["responsibilities"], 
                "qualifications": detailJson["qualifications"],
                "validThrough": detailJson["validThrough"]
            })
    except:
        pass
    
df = pd.DataFrame(results)
df.to_csv("job.csv", sep=',', encoding='utf-8')