'''
Creating an app for tracking prices of items in various websites.
Author: Batuhan Aktan
Date: DEC 2020
'''
from tkinter import *
import requests
import pandas as pd
import bs4
from openpyxl import *
import mysql.connector



HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
db = mysql.connector.connect(
    host="us-cdbr-east-02.cleardb.com",
    user="b27e5970f2d789",
    passwd="0c7dd0cf",
    database="heroku_cbaa81f3b8e025a"
    )
cursor  = db.cursor()
def linkCheck():
    url = entry.get()
    itemID = url[-10:]
    price = ''
    html = requests.get(url, headers=HEADERS) 
    content = bs4.BeautifulSoup(html.content, features='lxml')
    try:
        priceText = content.find(id='priceblock_dealprice').get_text()
        name = content.find(id="title").get_text()
    except:
        priceText = content.find(id='priceblock_ourprice').get_text()
        name = content.find(id="title").get_text()
    for element in priceText:
        if element.isnumeric() or element == '.':
            price += element
    try:
        float(price)
        return True, price, name, itemID, url
    except:
        return False

def save():
    email = entryTwo.get()
    passwd = entry.get()
    if True:
        cursor.execute("SELECT userEmail FROM userdb")
        for i in cursor:
            print(i[0])
            print(email)
            if i[0] == email:
                print("User Already Has an account")
                return
        cursor.execute("INSERT INTO userdb (iduserDB, userEmail, userPass) VALUES (%s,%s,%s)",(6, email, passwd))
        db.commit()
            
    else:
        print("That Link is not Valid!, Try Again.")
    

root = Tk()
entry = Entry(root)
entryTwo = Entry(root)
entryTwo.pack()
entry.pack()

myButton = Button(root, text="Submit", command=save)
myButton.pack()

root.mainloop()

