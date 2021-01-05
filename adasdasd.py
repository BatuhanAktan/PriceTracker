import mysql.connector

db = mysql.connector.connect(
    host="us-cdbr-east-02.cleardb.com",
    user="b27e5970f2d789",
    passwd="0c7dd0cf",
    database="heroku_cbaa81f3b8e025a"
    )
cursor = db.cursor()
print("INSERT INTO userdb (iduserDB ,userid, userEmail, userPass) VALUES ({},{},{},{});".format(2398, 'asde', 'ade', 'adeas'))
cursor.execute("INSERT INTO userdb (iduserDB, userid, userEmail, userPass) VALUES ({},'{}','{}','{}');".format(2398, 'asde', 'ade', 'adeas'))
print('true')
db.commit()
