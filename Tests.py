import mysql.connector
import os
import hashlib
import bs4
import requests
'''
db = mysql.connector.connect(
    )
'''
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

html = requests.get("https://www.amazon.ca/beyerdynamic-990-PRO-Headphones-Open-Back-Construction/dp/B07KFN5LL4/?_encoding=UTF8&pd_rd_w=zPft2&pf_rd_p=ab3c85e7-dd66-41c2-8070-fe9b2dd6dada&pf_rd_r=N4G8VSS93A62DV3WY3NM&pd_rd_r=a072ece0-7bfe-410b-9c49-366ca6a1593e&pd_rd_wg=9Ug6R&ref_=pd_gw_ci_mcx_mr_hp_d", headers=HEADERS) 
content = bs4.BeautifulSoup(html.content, features='lxml')
imgUrl = content.find(id="landingImage").decode('utf-8')
loc1, loc2 = 0, 0
print(len(imgUrl))
for i in range(len(imgUrl)):
	print(i)
	if imgUrl[i] == '{':
		loc1 = i
	elif  imgUrl[i] == ',':
		loc2 = i
		break

print(loc1,loc2)
