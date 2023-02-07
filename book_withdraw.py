from numpy import datetime64
import pymysql
import datetime
from datetime import timedelta
from datetime import date
from pymysql import NULL
from datetime import date
from dateutil.relativedelta import relativedelta
from book_borrow import*
from delete_reserve import *
from NEW import*
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


def validatedeletebook(accessionid):
    if not book_exist(accessionid):
        return (False,"book does not exist")
    if not notborrowed(accessionid):
        return (False,"access denied book borrowed")
    if not notreserved(accessionid):
        return (False, "access denied book reserved")
    return (True, "withdraw book")
    
def deletebook(accessionid):
    local_session = session(bind = engine)
    local_session.query(Book).filter(Book.accessionNo == accessionid).delete()  
    local_session.commit()
    return (True,"Success Book Withdrawn")
