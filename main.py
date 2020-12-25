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



HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


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
    cond, price, name, itemID, link = linkCheck()
    print(cond, price, name, itemID, link )
    if cond:
        workbook  = load_workbook(filename="Data.xlsx")
        sheet = workbook.active
        for cell in sheet["C"]:
            if cell.value == itemID:
                return
        row = sheet.max_row+1
        sheet["C"+str(row)] = itemID
        sheet["D"+str(row)] = name
        sheet["E"+str(row)] = price
        sheet["F"+str(row)] = link
        workbook.save(filename="Data.xlsx")
    else:
        print("That Link is not Valid!, Try Again.")
    

root = Tk()
entry = Entry(root)
entry.pack()

myButton = Button(root, text="Submit", command=save)

myButton.pack()

root.mainloop()

