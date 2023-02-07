import pymysql
from datetime import date

from pymysql import NULL
import fine_payment


con = pymysql.connect(host='localhost',
        user='root',
        password='Duanyaoyi1209',
        db='ALibrarySystem',
        cursorclass=pymysql.cursors.DictCursor)
cursor = con.cursor()
def create_connection():
    con = pymysql.connect(host='localhost',
        user='root',
        password='Duanyaoyi1209',
        db='ALibrarySystem',
        cursorclass=pymysql.cursors.DictCursor)
    return con
def display_outstandingfine():
    con = create_connection()
    cursor = con.cursor()
    find_members = ("SELECT * FROM Membership WHERE memberID IN (SELECT memberID FROM Fine WHERE amount > 0);")
    cursor.execute(find_members)

    result = cursor.fetchall()
    for row in result:
        print(row)
        print("\n") 
    return result

display_outstandingfine()
