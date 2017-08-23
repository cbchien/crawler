# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 16:32:51 2017

@author: cbchien

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

results = []

url = 'http://fontawesome.io/icons/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
allResult = soup.findAll('i',{'class':'fa'})
maxNum = len(allResult)

for i in range(0,maxNum):
    results.append(allResult[i]['class'])

df = pd.DataFrame(results)
df.to_csv("fontawesome.csv", sep=',', encoding='utf-8')
