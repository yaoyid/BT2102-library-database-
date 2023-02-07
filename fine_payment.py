from numpy import datetime64
import pymysql
import datetime
from datetime import timedelta
from datetime import date
from pymysql import NULL
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import false


con = pymysql.connect(host='localhost',
        user='root',
        password='Duanyaoyi1209',
        db='ALibrarySystem',
        cursorclass=pymysql.cursors.DictCursor)
def create_connection():
    con = pymysql.connect(host='localhost',
        user='root',
        password='Duanyaoyi1209',
        db='ALibrarySystem',
        cursorclass=pymysql.cursors.DictCursor)
    return con
cursor = con.cursor()

def member_exists(id):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT COUNT(*) FROM Fine WHERE memberID = %s;"
    cursor.execute(comment, id)
    result = cursor.fetchall()
    fine = list(result[0].values())[0]
    if fine == 0:
        return False
    return True

def acquire_fine(id):
    if member_exists(id):
        con = create_connection()
        cursor = con.cursor()
        comment = "SELECT amount FROM Fine WHERE memberID = %s;"
        cursor.execute(comment, id)
        result = cursor.fetchall()
        fine = list(result[0].values())[0]
        print(fine)
        return fine
    return False

def fine_payment(id, amount):
    con = create_connection()
    cursor = con.cursor()
    if amount == acquire_fine(id):
        clear_fine = ("UPDATE Fine SET amount = 0, paymentDate = CURDATE() WHERE memberID = %s;")
    
        cursor.execute(clear_fine, id)
        con.commit()
        con.close()
        print ("done")
        return (True)
    else:
        return (False)



