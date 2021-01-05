'''
Creating an app for tracking prices of items in various websites.
Author: Batuhan Aktan
Date: JAN 2021
'''
import kivy 
import requests
import pandas as pd
import bs4
import mysql.connector
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
import re
#vars
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
    regex ='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex2 ='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if (re.search(regex,email)) or (re.search(regex2,email)):
        return True
    else:
        return False
def save():
    email = entryTwo.get()
    passwd = entry.get()
    if True:
        cursor.execute("SELECT userEmail FROM userdb")
        for i in cursor:
            if i[0] == email:
                print("User Already Has an account")
                return
        cursor.execute("INSERT INTO userdb (iduserDB, userEmail, userPass) VALUES (%s,%s,%s)",(6, email, passwd))
        db.commit()
            
    else:
        print("That Link is not Valid!, Try Again.")


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
    def check(self, uid, passw):
        print("run")
        cursor.execute("SELECT userEmail FROM userdb WHERE userEmail = '{}';".format(uid))
        dbEmail = [x[0] for x in cursor]
        if len(dbEmail) == 0:
            print(dbEmail)
            return False
        else:
            cursor.execute("SELECT userPass FROM userdb WHERE userEmail = '{}';".format(uid))
            dbPassw = [x[0] for x in cursor]
            print(dbEmail[0], dbPassw[0], uid, passw)
            if dbPassw[0] == passw:
                return True
            else:
                return False
    def add(self, uid, email, passw, passw2):
        print('run2')
        print(passw, passw2)
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
            print(type(valueList[0]), uid, email, passw)
            cursor.execute("INSERT INTO userdb (iduserDB ,userid, userEmail, userPass) VALUES ({},'{}','{}','{}');".format(str(valueList[0]+1), uid, email, passw))
            db.commit()
            return True
        print('general false')
        return False
PriceTracker().run()

'''
#AppDesign
class MainScreen(Screen):
    pass

class LogScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("screens.kv")


class MyApp(App):
    def build(self):
        return kv
    def popUp(self):
        toast("Wrong Password, Try again!")
    def passwCheck(self,uid,passw):
        email = cursor.execute("SELECT userEmail FROM userdb WHERE userEmail = (%s)", uid)
        

#Running
if __name__ == "__main__":
    MyApp().run()

    

root = Tk()
entry = Entry(root)
entryTwo = Entry(root)
entryTwo.pack()secondScreen
entry.pack()

myButton = Button(root, text="Submit", command=save)
myButton.pack()

root.mainloop()
'''
