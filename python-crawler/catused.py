# -*- coding: utf-8 -*-
import requests
import re
import csv
import json

results = []
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1011_38_&et=_1011_55_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1011_38_&et=_1011_55_&mfc=100&srg=_1_SWUS_&pnr=2&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1011_38_&et=_1011_55_&mfc=100&srg=_1_SWUS_&pnr=3&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1011_38_&et=_1011_55_&mfc=100&srg=_1_SWUS_&pnr=4&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=2&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=3&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=4&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=5&epp=90&sf=relevance&so=false"]

for url in urls:
    a = requests.get(url)
    maxnum = len(results)
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(a.text, 'html.parser')
    
    allitem = soup.find_all("span", {"itemprop":"name"}, True)
    for name in allitem:
        results.append({
                    "name": name['content']
                    })
    print("Total of ",  len(allitem))
    print("start ", maxnum)
    print("End ", (maxnum + len(allitem)))
    for item in range(maxnum, (maxnum + len(allitem))):
        print(item)
        print((item-maxnum))
        results[item]["category"] = soup.find_all("span", {"itemprop":"category"}, True)[item-maxnum].text
        results[item]["url"] = soup.find_all("span", {"itemprop":"url"}, True)[item-maxnum]['content']
        results[item]["price"] = re.sub('[\s+]', '', soup.find_all("li", {"class" : "final"}, True)[item-maxnum].text)
        results[item]["hour"] = re.sub('[\s+]', '', soup.find_all("p", {"class" : "hours"}, True)[item-maxnum].text)
        results[item]["year"] = re.sub('[\s+]', '', soup.find_all("p", {"class" : "year"}, True)[item-maxnum].text)
        results[item]["location"] = re.sub('[\s+]', '', soup.find_all("p", {"class" : "Location"}, True)[item-maxnum].text)



jsondata = str(results).replace("'",'"')
print(jsondata)
x = json.loads(jsondata)
f = csv.writer(open("test.csv", "w+"))
for x in x:
    f.writerow([x["name"],
                x["category"],
                x["hour"],
                x["price"],
                x["year"],
                x["location"],
                x["url"]])
    
'''
Track Excavators
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1005_152551_&et=_1005_77_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1005_152551_&et=_1005_77_&mfc=100&srg=_1_SWUS_&pnr=2&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1005_152551_&et=_1005_77_&mfc=100&srg=_1_SWUS_&pnr=3&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1005_152551_&et=_1005_77_&mfc=100&srg=_1_SWUS_&pnr=4&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1005_152551_&et=_1005_77_&mfc=100&srg=_1_SWUS_&pnr=5&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1005_152551_&et=_1005_77_&mfc=100&srg=_1_SWUS_&pnr=6&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1005_152551_&et=_1005_77_&mfc=100&srg=_1_SWUS_&pnr=7&epp=90&sf=relevance&so=false"]

Backhoe Loaders
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1003_9_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1003_9_&mfc=100&srg=_1_SWUS_&pnr=2&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1003_9_&mfc=100&srg=_1_SWUS_&pnr=3&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1003_9_&mfc=100&srg=_1_SWUS_&pnr=4&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1003_9_&mfc=100&srg=_1_SWUS_&pnr=5&epp=90&sf=relevance&so=false"]

Forklifts
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1023_91_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1023_91_&mfc=100&srg=_1_SWUS_&pnr=2&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1023_91_&mfc=100&srg=_1_SWUS_&pnr=3&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1023_91_&mfc=100&srg=_1_SWUS_&pnr=4&epp=90&sf=relevance&so=false"]

Motor Graders
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1007_36_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1007_36_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false"]

Track Loaders
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1013_63_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false"]

Track Type Tractors
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1014_66_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1014_66_&mfc=100&srg=_1_SWUS_&pnr=2&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1014_66_&mfc=100&srg=_1_SWUS_&pnr=3&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1014_66_&mfc=100&srg=_1_SWUS_&pnr=4&epp=90&sf=relevance&so=false"]

Skid Steel Loaders
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1011_38_&et=_1011_55_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1011_38_&et=_1011_55_&mfc=100&srg=_1_SWUS_&pnr=2&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1011_38_&et=_1011_55_&mfc=100&srg=_1_SWUS_&pnr=3&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1011_38_&et=_1011_55_&mfc=100&srg=_1_SWUS_&pnr=4&epp=90&sf=relevance&so=false"]

Wheel Loader
urls = ["http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=1&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=2&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=3&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=4&epp=90&sf=relevance&so=false",
        "http://catused.cat.com/en/search_results_wide.html?et=_1016_152504_&et=_1016_79_&mfc=100&srg=_1_SWUS_&pnr=5&epp=90&sf=relevance&so=false"]

'''


