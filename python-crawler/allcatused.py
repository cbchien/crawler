# -*- coding: utf-8 -*-
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
"""
@author: cbchien
"""

results = []
for i in range(0,243):
    url = "http://catused.cat.com/en/search_results_wide.html?mfc=100&pnr="+str(i)+"&epp=90&sf=relevance&so=false"
    
    a = requests.get(url)
    maxnum = len(results)
    
    soup = BeautifulSoup(a.text, 'html.parser')
    
    allitem = soup.find_all("span", {"itemprop":"name"}, True)
    for name in allitem:
        results.append({
                    "name": name['content']
                    })
    print("End ", (maxnum + len(allitem)))
    c = soup.find_all("span", {"itemprop":"category"}, True)
    u = soup.find_all("span", {"itemprop":"url"}, True)
    p = soup.find_all("li", {"class" : "final"}, True)
    h = soup.find_all("p", {"class" : "hours"}, True)
    y = soup.find_all("p", {"class" : "year"}, True)
    l = soup.find_all("p", {"class" : "Location"}, True)
    for item in range(maxnum, (maxnum + len(allitem))):
        results[item]["category"] = c[item-maxnum].text
        results[item]["url"] = u[item-maxnum]['content']
        results[item]["price"] = re.sub('[\s+]', '', p[item-maxnum].text)
        results[item]["hour"] = re.sub('[\s+]', '', h[item-maxnum].text)
        results[item]["year"] = re.sub('[\s+]', '', y[item-maxnum].text)
        results[item]["location"] = re.sub('[\s+]', '', l[item-maxnum].text)

df = pd.DataFrame(results)

df.to_csv("catused_all.csv", sep=',', encoding='utf-8')
