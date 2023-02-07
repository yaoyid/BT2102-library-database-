from datetime import datetime, timedelta
from datetime import date
from logging import makeLogRecord
from os import access
from pickletools import read_uint1
from re import M
import string
from threading import local
from book_borrow import *
from fine_payment import *
from sqlalchemy import  select, and_
from NEW import Membership, Book, Author, Fine, BookReservation, BookLoan, engine, session, base
import pymysql
from datetime import date



from pymysql import NULL

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

def update_member_name(id,name):
    local_session = session(bind = engine)
    local_session.query(Membership).filter(Membership.memberID ==id).update({"name": name})
    local_session.commit()
    return 

def update_member_faculty(id,faculty):
    local_session = session(bind = engine)
    local_session.query(Membership).filter(Membership.memberID ==id).update({"faculty": faculty})
    local_session.commit()
    return 

def update_member_phone(id,phone):
    local_session = session(bind = engine)
    local_session.query(Membership).filter(Membership.memberID ==id).update({"telNo": phone})
    local_session.commit()
    return 

def update_member_email(id,email):
    local_session = session(bind = engine)
    local_session.query(Membership).filter(Membership.memberID ==id).update({"eMail": email})
    local_session.commit()
    return 



def reservecount(memberid):
    return len(session(bind = engine).query(BookReservation).filter(BookReservation.memberID == memberid).all()) < 2
def isbeingreserve(a):
    return len(session(bind = engine).query(BookReservation).filter(BookReservation.accessionNo == a).all()) > 0


def isborrow(accessionid):
    a = select(*BookLoan.__table__.columns).where(BookLoan.accessionNo == accessionid)
    local_session = session(bind = engine)
    aa = None
    for i in local_session.execute(a):
        aa = i[-1]
    if aa is None:
        return False
    return True 

def isreserve(accessionid, memberid):
    a = select(*BookReservation.__table__.columns).where(BookReservation.accessionNo == accessionid)
    local_session = session(bind = engine)
    b = local_session.execute(a)
    if not b.all():
        return "yes"
    for i in local_session.execute(a):
        if i[-1] == memberid:
            return 'borrow'

    return "cannot borrow"



    





def deletemember(memberid):
    if len(session(bind = engine).query(BookLoan).filter(BookLoan.memberID == memberid).all()) > 0:
        return "book"
    if acquire_fine(memberid):
        return "fine"
    if has_reservation(memberid):
        local_session = session(bind=engine)
        local_session.query(BookReservation).filter(BookReservation.memberID == memberid).delete()
        local_session.commit()
    try:
        local_session = session(bind=engine)
        local_session.query(Membership).filter(Membership.memberID == memberid).delete()
        local_session.commit()
        return "yes"
    except:
        return "no"
    

def deletebook(accessionid):
    if notborrowed(accessionid) == False:
        return (False,"access denied book borrowed")
    if notreserved(accessionid):
        return (False, "access denied book reserved")
    local_session = session(bind = engine)
    local_session.query(Book).filter(Book.accessionNo == accessionid).delete()  
    local_session.commit()
    return (True,"Success Book Withdrawn")

def info(accessionid, memberid):
    try:
        local_session = session(bind = engine)
        duedate = datetime.now().date() + timedelta(14)
        m = local_session.query(Membership).with_entities(Membership.memberID,Membership.name).filter(Membership.memberID == memberid).first()
        b = local_session.query(Book).with_entities(Book.accessionNo,Book.title).filter(Book.accessionNo == accessionid).first()
        
        return (True,{ 'memberid' : m.memberID, 'name' : m.name, 'bookid': b.accessionNo, 'title' : b.title, 'bdate' : datetime.datetime.date(),  'ddate' : duedate})
    except:
        return (False,'Missing or incomplete fields')
def info1(accessionid,dat):
    try:
        dat = datetime.strptime(dat, '%Y-%m-%d').date()
        local_session = session(bind = engine)
        b = local_session.query(BookLoan).with_entities(BookLoan.accessionNo, BookLoan.memberID).filter(BookLoan.accessionNo == accessionid).first()
        if b != []:
            m = local_session.query(Membership).with_entities(Membership.memberID,Membership.name).filter(Membership.memberID == b.param_1).first()
            bb = local_session.query(Book).with_entities(Book.accessionNo,Book.title).filter(Book.accessionNo == b.accessionid).first()
            return (True, {'memberid' : m.memberID, 'name' : m.name, 'bookid': bb.accessionNo, 'title' : bb.title, 'rdate' : f'{dat.date()}'})
        else:
            return (False, 'Book not borrowed')
    except:
        return (False, 'Missing or incomplete fields')

def info2(accessionid, memberid):
    try:
        local_session = session(bind = engine)
        m = local_session.query(Membership).with_entities(Membership.memberID,Membership.name).filter(Membership.memberID == memberid).first()
        b = local_session.query(Book).with_entities(Book.accessionNo,Book.title).filter(Book.accessionNo == accessionid).first()
        return (True,[m.memberID,m.name,b.accessionNo,b.title])
    except:
        return(False, "Missing or in complete fields")

        




def borrow(accessionid, memberid):
    try:
        if member_exists(memberid) and acquire_fine(memberid) > 0:
            return (False,'Access denied pay fine')
        if not notborrowed(accessionid):
            a = select(*BookLoan.__table__.columns).where(BookLoan.accessionNo == accessionid)
            local_session = session(bind = engine)
            a = local_session.execute(a).first()
            duedate = a[2].date()
            return (False,f"Access denied book on loan until {duedate}")
        if overdue_book(id):
            return (False, "please return overdue book!")
        if not memberCanBorrow(memberid):
            return "borrow two books"
        if not notreserved(accessionid):
            if not memberReserved(memberid, accessionid):
                return (False,'Access denied book on reservation')

        else:
            book_borrow(memberid, accessionid)
            return (True,)
               
    except:
        return (False,'Access denied invalid input')

def returning(accessionid, datereturn):
    local_session = session(bind = engine)
    a = select(*BookLoan.__table__.columns).where(BookLoan.accessionNo == accessionid)
    a = local_session.execute(a).first()
    dat = datetime.strptime(datereturn, '%Y-%m-%d').date()
    if a:
        #m = (dat.date() - a[1].date()).days - 14
        #if m > 0:
        if a[2] < dat:
            fin = local_session.query(Fine).with_entities(Fine.amount).filter(Fine.memberID == a[3]).first()
            local_session.query(Fine).filter(Fine.memberID == a[3]).update({'amount' : fin.amount + (dat - a[2]).days})
        local_session.query(BookLoan).filter(and_(BookLoan.accessionNo == accessionid)).delete()
        local_session.commit()
        return (True, "Book returned")
    return (False, "Book not borrowed")
