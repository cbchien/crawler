# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 09:46:40 2017

@author: user
"""

import requests
# import pandas as pd
# import numpy as np
from pyquery import PyQuery as pq
import re

chrome_cookie = 'Cookie: COOKIE_SUPPORT=true; optimizelyEndUserId=oeu1508471708751r0.5540590619158643; JSESSIONID=936EEB350EFC6E43ABAC186A5D72093A.fry05; COMPANY_ID=10106; ID=4f3835334d6f4d43664f6573534a4631685148464a413d3d; PASSWORD=7736504f306d30594c702b73534a4631685148464a413d3d; SCREEN_NAME=48644a7453574644414b416a4d4f31534f744a662f50664938366737526a4f586255764a6a52632f2b6f6f3635426d6e6271476732346e6370334c2f4a6f657445524b55556f346970724b733779655076516d764f302f5063537a482f355252; RING_WELL=asbrporsilpbibigllmo; CURRENT_ACCOUNT_INDEX_7lZdYxuAoF0FUhN0DwaXjg%3D%3D=10239997; optimizelySegments=%7B%221406976578%22%3A%22false%22%2C%221406976579%22%3A%22gc%22%2C%221406976580%22%3A%22referral%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.2.1442720675.1508471709; _gid=GA1.2.35423416.1508471709; _dc_gtm_UA-231124-1=1; _mkto_trk=id:875-YYZ-477&token:_mch-rbauction.com-1508471709444-73713; UI_UID=7lZdYxuAoF0FUhN0DwaXjg==; UI_STATE=hard login; __hstc=2906543.bf126abbceb1c384bb104257a4840610.1508471710857.1508471710857.1508471710857.1; __hssrc=1; __hssc=2906543.8.1508471710858; hubspotutk=bf126abbceb1c384bb104257a4840610; GUEST_LANGUAGE_ID=en_US; GUEST_COUNTRY=United+States; GUEST_LANGUAGE=English; GUEST_FLAG=us; optimizelyPendingLogEvents=%5B%22n%3Doptly_activate%26u%3Doeu1508471708751r0.5540590619158643%26wxhr%3Dtrue%26time%3D1508473541.648%26f%3D9014394112%2C8928963444%2C9032631573%2C8894811869%26g%3D%22%5D'

cookie_to_dict = lambda s: {k.strip():v for k,v in re.findall(r'(.*?)=(.*?);', s.split(':')[1])}

url_parent = 'https://www.rbauction.com/2013-CATERPILLAR--HYDRAULIC-EXCAVATORHEX_9445826/?invId=9445826&id=ar&auction=RALEIGH-DURHAM-NC-2016245'
ses = requests.session()
cookie = cookie_to_dict(chrome_cookie)
ses.cookies = requests.cookies.cookiejar_from_dict(cookie)

response = ses.get(url_parent)
d = pq(response.text)
c = d('#dei-pane div.rba-content-column')

result = dict( (k.text_content().strip(), v.text_content().strip()) \
				for k, v in list(zip(c[::2], c[1::2])))
print(result)

with open('test.html', 'wt', encoding='utf-8') as f:
	f.write(response.text)

# print(response.text)
# print(response)