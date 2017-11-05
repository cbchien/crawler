import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

results = []
listingPerPage = 100

for page in range(0,3):
    weburl="https://www.mascus.com/Caterpillar+320+EL/auctions%3d1/+/"+str(page+1)+","+str(listingPerPage)+",relevance,search.html"
    print(weburl)
    a = requests.get(weburl)
    print('Status Code',a.status_code)
    soup = BeautifulSoup(a.text, 'html.parser')
    
    resultItems = soup.find_all("li", {"class":"single-result"}, True)
    priceItems = soup.find_all("div", {"class":"result-price"}, True)
    
    for item in range(0, len(resultItems)):
        '''
        print(item + page*listingPerPage)
        '''
        name = resultItems[item].find("h3", {"class":"result-title"}).find("a", {"class":"title-font"}).text
        category = resultItems[item].find("p", {"class":"result-details"}).find("br").previousSibling
        price = priceItems[item].text
        
        try:
            hour = resultItems[item].find("p", {"class":"result-details"}).find("i", {"class":"fa fa-cogs"}).nextSibling
        except:
            hour = "N/A"
        
        try:
            year =  resultItems[item].find("p", {"class":"result-details"}).find("i", {"class":"fa fa-calendar"}).nextSibling
        except:
            year = "N/A"
        
        try:
            location =  resultItems[item].find("p", {"class":"result-details"}).find("i", {"class":"fa fa-map-marker"}).nextSibling
        except:
            location = "N/A"
    
        try:
            url = resultItems[item].find("h3", {"class":"result-title"}).find("a", {"class" :"title-font"})['href']
        except:
            pass    
        
        results.append({
                'index':item + page*listingPerPage,
                'name':name,
                'category':category,
                'hour':hour,
                'price':price,
                'year':year,
                'location':location,
                'url':url
                })
    
jsondata = re.sub("\'\w{1}\s",'!',str(results)).replace("'",'"').replace('"- New','- New')

df = pd.DataFrame(results)

import datetime as dt     
df['scrape_date'] = dt.date.today
df.to_csv("mascus.csv", sep=',', encoding='utf-8')
