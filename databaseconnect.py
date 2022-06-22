import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="py"
)

mycursor = db.cursor()
mycursor.execute("update swipe set swipeWhere=1")
db.commit()
mycursor.execute("select * from swipe")

for x in mycursor:
    print(x[0])
