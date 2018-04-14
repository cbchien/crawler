# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 17:43:47 2018

@author: cbchien
"""

import requests
import re
import json
from bs4 import BeautifulSoup

results = {}

# Parse main items page
main_url = "https://www.mhchinese.wiki/items"
item_page_content = requests.get(main_url)
soup = BeautifulSoup(item_page_content.text, 'html.parser')

# Collects all category urls
# https://www.mhchinese.wiki + {entry_url}
category_urls = []
first_list_category_entries = soup.find("ul", {"class":"link-list"}, True).find_all("a", True)
for entry in first_list_category_entries:
    category_urls.append({
            'title' : entry.text,
            'url' : entry['href']
    })
 
    # Parse item in each url in category url
for url in category_urls:
    item_url = 'https://www.mhchinese.wiki' + url['url']
    print('Getting ready for', url['title'], item_url)
    item_url_content = requests.get(item_url)
    item_soup = BeautifulSoup(item_url_content.text, 'html.parser')
    list_of_items = item_soup.find_all("a", {"class":"tip"}, True)
    
    # other fields
    category = url['title']
    
    # Array to hold item url in each categories
    list_urls = []
    
    for item in list_of_items:
        list_urls.append({
                'item_url': item['href'],
                'item_title': item.text
                })

    # loop through url in list_url to parse details
    for url in list_urls:
        detail_url = 'https://www.mhchinese.wiki' + url['item_url']
        print('----------',len(results),'----------')
        print('Parsing details in page:', url['item_title'], url['item_url'])
        detail_page_content = requests.get(detail_url)
        detail_soup = BeautifulSoup(detail_page_content.text, 'html.parser')
        
        # item table 
        item_table = detail_soup.find('table', {'class':'item-table'}, True).find_all("td")
        item_table_name = item_table[0].find('span').text
        item_table_jpn_name = re.sub('<br />英文:','',item_table[0].find('span')['title'])
        item_table_rare_index = item_table[1].text
        item_table_max_index = item_table[2].text
        item_table_price = item_table[3].text
        item_table_description = item_table[4].text
        print('Now adding', item_table_name, item_table_rare_index, item_table_max_index, item_table_price, item_table_description)
        
        # simple talbe
        sudo_simple_table = []
        try:
            simple_table = detail_soup.find('table', {'class':'simple-table'}, True)
            simple_table_rows = simple_table.find('td').find_all('span',{'class':'tip'}, True)

            for row in simple_table_rows:
                simple_table_position = row.previousSibling.replace('\n','').replace(' ','')
                simple_table_map = row.text
                simple_table_spot = row.nextSibling.nextSibling.text
                simple_table_spot_url = row.nextSibling.nextSibling['href']
                sudo = simple_table_position + ' ' + simple_table_map + ' ' + simple_table_spot
                sudo_simple_table.append(sudo)
        except:
            pass
        print('with location', sudo_simple_table)
        
        # Update item details as {} in results {}
        try:
            results[item_table_name]
            results[item_table_name]['Category'] += ',' + category
            print('Found existing entry. Append new info to category section')
        except:
            results.update({
                    item_table_name: {
                        'Title': item_table_name,
                        'Japanese': item_table_jpn_name,
                        'Info': {
                            'get-location': sudo_simple_table
                        },
                        'Category': category,
                        'Price': item_table_price,
                        'Rare': item_table_rare_index,
                        'Description': item_table_description
                        }
                    })
            print('Successfully updated', item_table_name)
        
# Retrun json string
def obj_dict(obj):
    return obj.__dict__

# Conver Results object to json string format
print('Converting result object of objects to json string...')
json_string = json.dumps(results, default=obj_dict, ensure_ascii=False)

# Save file to output.txt
print('Saving results json string to file...')
with open('output.txt', 'w', encoding="utf-8") as f:
    f.write(json_string)
    print('File saved!')