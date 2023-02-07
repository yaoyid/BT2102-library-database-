from numpy import datetime64
import pymysql
import datetime
from datetime import timedelta
from datetime import date
from pymysql import NULL
from datetime import date
from dateutil.relativedelta import relativedelta
from fine_payment import *


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


def update_fine(date, bookNo, id):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT DATEDIFF(CAST(%s AS DATE), dueDate) FROM BookLoan WHERE accessionNo = %s;"
    cursor.execute(comment, (date, bookNo))
    result = cursor.fetchall()
    print(result)
    if result:
        fine = list(result[0].values())[0]* 1

        if fine > 0 :
            new_fine = acquire_fine(id) + fine
            add_fine = ("UPDATE Fine SET amount = (%s) WHERE memberID = %s;")
            data_fine = (new_fine, id)
            cursor.execute(add_fine, data_fine)
            con.commit()
            con.close()
            print("added fine")
            return new_fine
        return acquire_fine(id)


def book_return(date, bookNo, id):
    con = create_connection()
    cursor = con.cursor()
    update_fine(date, bookNo, id)
    
    con = create_connection()
    cursor = con.cursor()
    
    comment = "DELETE FROM BookLoan WHERE accessionNo = %s AND memberID = %s"
    cursor.execute(comment, (bookNo, id))
    con.commit()
    con.close()
    print("returned book")
    

