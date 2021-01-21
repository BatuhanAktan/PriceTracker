'''
Creating an app for tracking prices of items in various websites.
Author: Batuhan Aktan
Date: JAN 2021
'''
import os
import requests
import pandas as pd
import bs4
import mysql.connector
import re
import hashlib
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager


#vars
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


db = mysql.connector.connect(
    )


sha = hashlib.sha256()
sha2 = hashlib.sha256()



cursor  = db.cursor()


#Backend
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


def emailCheck(email):
	'''
	This function if the user entered a valid email
	Parameters: email - string of entered email.
	return: Boolean according to email validity
	'''

    regex ='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex2 ='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    if (re.search(regex,email)) or (re.search(regex2,email)):

        cursor.execute('SELECT userEmail from userdb')

        userEmails = [x[0] for x in cursor] # Checking if the user email is already in the db

        for element in userEmails:
            if element == email:
                return False

        return True

    return False

class MainPage(Screen):
    pass
class LogInPage(Screen):
    pass
class SignUp(Screen):
    pass


sm = ScreenManager()

sm.add_widget(MainPage(name='LogIn'))

sm.add_widget(MainPage(name='main'))

sm.add_widget(MainPage(name='signup'))


class PriceTracker(MDApp):


    def build(self):

        kv = Builder.load_file("PriceTracker.kv")
        return kv


    def check(self, email, passw):

        email = email.strip()
        email = "b'{}'".format(email)
        email = email.encode('utf-8')
        email = sha.update(email).hexdigest()

        passw = "b'{}'".format(passw)
        passw = passw.encode('utf-8')
        passw = sha2.update(passw).hexdigest()

        cursor.execute("SELECT userEmail FROM userdb WHERE userEmail = '{}';".format(uid))

        dbEmail = [x[0] for x in cursor]

        if len(dbEmail) == 0:
            return False

        else:

            cursor.execute("SELECT userPass FROM userdb WHERE userEmail = '{}';".format(uid))
            dbPassw = [x[0] for x in cursor]

            if dbPassw[0] == passw:
                return True

            else:
                return False


    def add(self, uid, email, passw, passw2):

        uid = uid.strip()

        email = email.strip()
        email = "b'{}'".format(email)
        email = email.encode('utf-8')
        email = sha.update(email).hexdigest()

        passw = "b'{}'".format(passw)
        passw = passw.encode('utf-8')
        passw = sha2.update(passw).hexdigest()



        if uid == '' or email == '' or passw == '':
            return False


        if passw != passw2:
            print('false pass')
            return False


        if emailCheck(email):

            cursor.execute('SELECT userid FROM userdb')
            userIds = [x[0] for x in cursor]

            for element in userIds:
                if uid == element:
                    print('false uid')
                    return False

            cursor.execute('SELECT MAX(idUserDB) FROM userdb;')

            valueList = [x[0] for x in cursor]

            cursor.execute("INSERT INTO userdb (iduserDB ,userid, userEmail, userPass)\
             VALUES ({},'{}','{}','{}');".format(str(valueList[0]+1), uid, email, passw))

            db.commit()
            return True

        return False


PriceTracker().run()

