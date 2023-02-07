from numpy import datetime64
import pymysql
import datetime
from datetime import timedelta
from datetime import date
from pymysql import NULL
from datetime import date
from dateutil.relativedelta import relativedelta



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

def memberCanBorrow(id):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT IF ((SELECT COUNT(*) FROM BookLoan WHERE memberID = %s) < 2, 1, 0);"
    cursor.execute(comment, id)

    row = cursor.fetchall()
    if (list(row[0].values())[0]) == 1:
        return True
    return False  

def notborrowed(bookNo):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT IF ((SELECT COUNT(*) FROM BookLoan WHERE accessionNo = %s) = 0, 1, 0);"
    cursor.execute(comment, bookNo)

    row = cursor.fetchall()
    if (list(row[0].values())[0]) == 1:
        return True
    return False
def hasloan(id):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT IF ((SELECT COUNT(*) FROM BookLoan WHERE memberID = %s) > 0, 1, 0);"
    cursor.execute(comment, id)

    row = cursor.fetchall()
    if (list(row[0].values())[0]) == 1:
        return True
    return False  
hasloan("A101A")
def notreserved(bookNo):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT IF ((SELECT COUNT(*) FROM BookReservation WHERE accessionNo = %s) = 0, 1, 0);"
    cursor.execute(comment, bookNo)

    row = cursor.fetchall()
    if (list(row[0].values())[0]) == 1:
        return True
    return False


def memberReserved(id, bookNo):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT IF ((SELECT COUNT(*) FROM BookReservation WHERE accessionNo = %s AND memberID = %s) = 1, 1, 0);"
    cursor.execute(comment, (bookNo, id))

    row = cursor.fetchall()
    if (list(row[0].values())[0]) == 1:
        return True
    return False

def has_reservation(id):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT IF ((SELECT COUNT(*) FROM BookReservation WHERE memberID = %s) > 0, 1, 0);"
    cursor.execute(comment, id)

    row = cursor.fetchall()
    if (list(row[0].values())[0]) == 1:
        return True
    return False

def hasfine(id):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT IF ((SELECT amount FROM Fine WHERE memberID = %s) > 0, 1, 0);"
    cursor.execute(comment, id)

    row = cursor.fetchall()
    if (list(row[0].values())[0]) == 1:
        return True
    return False


def acquire_fine(id):
    con = create_connection()
    cursor = con.cursor()
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

def overdue_book(id):
    con = create_connection()
    cursor = con.cursor()
    comment = "SELECT DATEDIFF(NOW(), dueDate) FROM BookLoan WHERE memberID = %s;"
    cursor.execute(comment, id)

    result = cursor.fetchall()
    for row in result:
        if list(row.values())[0] > 0:
            print ("return book")
            return True
    print ("no overdue")
    return False

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

def book_borrow(id, bookNo):
    con = create_connection()
    cursor = con.cursor()
    while member_exists(id):
        if memberCanBorrow(id) == False:
            print ("member exceed borrowing limits")
            return (False, "member exceed borrowing limits")
        elif overdue_book(id):
            print ("please return overdue book!")
            return (False, "please return overdue book!")
        elif notborrowed(bookNo) == False:
            print ("book borrowed")
            return (False, "book borrowed")
        elif acquire_fine(id) > 0:
            print ("member has outstanding fine")
            return (False, "member has outstanding fine")
        elif notreserved(bookNo) == False :
            if memberReserved(id, bookNo) :
                delete = "DELETE FROM BookReservation WHERE accessionNo = %s AND memberID = %s"
                borrow = (bookNo, id)
                acquire = "INSERT INTO BookLoan (accessionNo, borrowDate, dueDate, memberID) VALUES (%s,CURDATE(), TIMESTAMPADD(DAY, 14, CURDATE()),  %s)" 
                cursor.execute(acquire, borrow)
                cursor.execute(delete, borrow)
                con.commit()
                con.close()
                print ("you have borrowed the book!")
                return (True, "you have borrowed the book!")
            else:
                print (False, "book reserved")
                return (False, "book reserved")
        else:
            borrow = (bookNo, id)
            acquire = "INSERT INTO BookLoan (accessionNo, borrowDate, dueDate, memberID) VALUES (%s,CURDATE(), TIMESTAMPADD(DAY, 14, CURDATE()),  %s)" 
            cursor.execute(acquire, borrow)
            con.commit()
            con.close()
            print ("you have borrowed the book!")
            return (True, "you have borrowed the book!")
 




