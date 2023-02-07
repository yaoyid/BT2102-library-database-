from datetime import datetime, timedelta
from datetime import date
from logging import makeLogRecord
from os import access
from pickletools import read_uint1
from re import M
import string
from threading import local
from book_borrow import *
from sqlalchemy import  select, and_
from NEW import Membership, Book, Author, Fine, BookReservation, BookLoan, engine, session, base
import pymysql
from datetime import date


import pymysql
from datetime import date

from pymysql import NULL

from book_borrow import memberReserved, notreserved

con = pymysql.connect(host='localhost',
        user='root',
        password='Duanyaoyi1209',
        db='ALibrarySystem',
        cursorclass=pymysql.cursors.DictCursor)
cursor = con.cursor()

def acquire_book(id, title, isbn, publisher, year, *authors):
    book = (id, title, isbn, publisher, year)
    acquire = ("INSERT INTO Book "
               "(accessionNo, title, isbn, publisher, yearPublished) "
               "VALUES (%s, %s, %s, %s, %s)") 
    cursor.execute(acquire, book)
    add_author = ("INSERT INTO Author "
               "(accessionNo, name) "
               "VALUES (%s, %s)")
    for author in authors:
        author_detail = (id, author)
        cursor.execute(add_author, author_detail)
    con.commit()
    con.close()

def create_member(id, name, telNo, faculty, email):
        data_member = (id, name, telNo, faculty, email)
        create = ("INSERT INTO Membership "
                "(memberID, name, faculty, telNo, eMail) "
                "VALUES (%s, %s, %s, %s, %s)") 
        add_fine = ("INSERT INTO Fine "
                "(memberID, paymentDate, amount) "
                "VALUES (%s, %s, %s)")
        data_fine = (id, date.today(), 0)

        cursor.execute(create, data_member)
        cursor.execute(add_fine, data_fine)
        con.commit()
        con.close()
       
def create_connection():
    con = pymysql.connect(host='localhost',
        user='root',
        password='Duanyaoyi1209',
        db='ALibrarySystem',
        cursorclass=pymysql.cursors.DictCursor)
    return con
cursor = con.cursor()

def book_search99(word,field):
    con = create_connection()
    cursor = con.cursor()
    query_book = ""
    search = word
    if field == "Author" or 'author':
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Author WHERE LOWER(name) REGEXP %s);"
        search = '^' + word.lower() + ' | ' + word.lower() +' | ' + word.lower() + '$'
    if field =="yearPublished":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE yearPublished = %s);"
    if field == "isbn":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE isbn = %s);"
    if field =="publisher":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE LOWER(publisher) REGEXP %s);"
        search = '^' + word.lower() + ' | ' + word.lower() +' | ' + word.lower() + '$' 
    if field =="title":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE LOWER(title) REGEXP %s);"
        search = '^' + word.lower() + ' | ' + word.lower() +' | ' + word.lower() + '$'
    if field == "accessionNo":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo = %s;"
    cursor.execute(query_book,word)
    result = cursor.fetchall()
    return result

def book_search(word,field):
    con = create_connection()
    cursor = con.cursor()
    query_book = ""
    search = word
    if field == "Author" or 'author':
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Author WHERE LOWER(name) REGEXP %s);"
        search = '^' + word.lower() + ' | ' + word.lower() +' | ' + word.lower() + '$'
    if field =="yearPublished":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE yearPublished = %s);"
    if field == "isbn":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE isbn = %s);"
    if field =="publisher":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE LOWER(publisher) REGEXP %s);"
        search = '^' + word.lower() + ' | ' + word.lower() +' | ' + word.lower() + '$' 
    if field =="title":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE LOWER(title) REGEXP %s);"
        search = '^' + word.lower() + ' | ' + word.lower() +' | ' + word.lower() + '$'
    if field == "accessionNo":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo = %s;"
    cursor.execute(query_book,word)
    result = cursor.fetchall()
    return result

def display_bookonloan():
    find_bookloan = "SELECT b.* , (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM BookLoan);"
    cursor.execute(find_bookloan)
    result = cursor.fetchall()
    return result

def display_bookonloan_tomember(id):
    find_bookonloan_tomember = ("SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM BookLoan WHERE memberID = %s );")
    cursor.execute(find_bookonloan_tomember, id)
    result = cursor.fetchall()
    return result
def display_bookreserved():
    find_bookreserved = ("SELECT br.accessionNo, b.title, br.memberID, br.reserveDate FROM BookReservation br Join Book b On br.accessionNo = b.accessionNo;")
    cursor.execute(find_bookreserved)
    result = cursor.fetchall()
    return result
def display_outstandingfine():
    find_members = ("SELECT * FROM Membership WHERE memberID IN (SELECT memberID FROM Fine WHERE amount > 0);")
    cursor.execute(find_members)
    result = cursor.fetchall()
    return result
def findmemberrrrrr(i):
        m = ("SELECT * FROM Membership WHERE memberID = %s")
        cursor.execute(m,i)
        result = cursor.fetchall()
        return result[0]
#print(findmemberrrrrr('A101'))

def update_member_name(id,name):
    local_session = session(bind = engine)
    local_session.query(Membership).filter(Membership.memberID ==id).update({"name": name})
    local_session.commit()
    local_session.close()
    return 

def update_member_faculty(id,faculty):
    local_session = session(bind = engine)
    local_session.query(Membership).filter(Membership.memberID ==id).update({"faculty": faculty})
    local_session.commit()
    local_session.close()
    return 

def update_member_phone(id,phone):
    local_session = session(bind = engine)
    local_session.query(Membership).filter(Membership.memberID ==id).update({"telNo": phone})
    local_session.commit()
    local_session.close()
    return 

def update_member_email(id,email):
    local_session = session(bind = engine)
    local_session.query(Membership).filter(Membership.memberID ==id).update({"eMail": email})
    local_session.commit()
    local_session.close()
    return 




def canborrow(memberid):
    #with con.cursor() as cur:
    #    a = cur.execute('SELECT COUNT(memberID) FROM Book WHERE memberID == memberid')
    #return a
    local_session = session(bind = engine)
    a = len(local_session.query(BookLoan).filter(BookLoan.memberID == memberid).all()) < 2
    local_session.close()
    return a
    


def reservecount(memberid):
    local_session = session(bind = engine)
    a = len(local_session.query(BookReservation).filter(BookReservation.memberID == memberid).all()) < 2
    local_session.close()
    return a
def isbeingreserve(a):
    local_session = session(bind = engine)
    aa =len(local_session.query(BookReservation).filter(BookReservation.accessionNo == a).all()) > 0
    local_session.close()
    return aa

def havefine(memberid,dat):
    local_session = session(bind=engine)
    a =select(*BookLoan.__table__.columns).where(BookLoan.memberID == memberid)
    l = []
    for y in local_session.execute(a):
        l.append(y)
        

    b = select(*Fine.__table__.columns).where(Fine.memberID == memberid)
    d = []
    for i in local_session.execute(b):
        d.append(i)
    
    dat = datetime.strptime(dat + f' {datetime.now().time().replace(microsecond=0)}', '%Y-%m-%d %H:%M:%S')
    for i in l:
        if dat.date() > i[1].date() + timedelta(14):
            local_session.close()
            return True
    for j in d:
        if j[2] != 0:
            local_session.close()
            return True
    local_session.close()
    return False

def isborrow(accessionid):
    a = select(*BookLoan.__table__.columns).where(BookLoan.accessionNo == accessionid)
    local_session = session(bind = engine)
    aa = None
    for i in local_session.execute(a):
        aa = i[-1]
    if aa is None:
        local_session.close()
        return False
    local_session.close()
    return True 

def isreserve(accessionid, memberid):
    a = select(*BookReservation.__table__.columns).where(BookReservation.accessionNo == accessionid)
    local_session = session(bind = engine)
    b = local_session.execute(a)
    if not b.all():
        local_session.close()
        return "yes"
    for i in local_session.execute(a):
        if i[-1] == memberid:
            local_session.close()
            return 'borrow'
    local_session.close()
    return "cannot borrow"

def getfineamt(memberid,d):
    local_session = session(bind = engine)
    a = select(*BookLoan.__table__.columns).where(BookLoan.memberID == memberid)
    l = []
    dat = datetime.strptime(d + f' {datetime.now().time().replace(microsecond=0)}', '%Y-%m-%d %H:%M:%S')
    for i in local_session.execute(a):
        l.append(i)
    
    b = select(*Fine.__table__.columns).where(Fine.memberID == memberid)
    p = []
    for i in local_session.execute(b):
        p.append(i)
     
    g = p[0][2]
    if l:
        for i in l:
            if dat.date() > (i[1] + timedelta(14).date()):
                local_session.close()
                return False
        local_session.close()
        return g
    local_session.close()
    return g


    





def deletemember(memberid):
    local_session = session(bind=engine)
    if len(local_session.query(BookLoan).filter(BookLoan.memberID == memberid).all()) > 0:
        local_session.close()
        return "book"
    if havefine(memberid,datetime.now().strftime("%Y-%m-%d")):
        local_session.close()
        return "fine"
    try:
        local_session.query(Membership).filter(Membership.memberID == memberid).delete()
        local_session.commit()
        local_session.close()
        return "yes"
    except:
        return "no"


def deletebook(accessionid):
    if isborrow(accessionid):
        return (False,"access denied book borrowed")
    if isbeingreserve(accessionid):
        return (False, "access denied book reserved")
    local_session = session(bind = engine)
    local_session.query(Book).filter(Book.accessionNo == accessionid).delete()  
    local_session.commit()
    local_session.close()
    return (True,"Success Book Withdrawn")

def info(accessionid, memberid):
    try:
        local_session = session(bind = engine)
        duedate = datetime.now().date() + timedelta(14)
        m = local_session.query(Membership).with_entities(Membership.memberID,Membership.name).filter(Membership.memberID == memberid).first()
        b = local_session.query(Book).with_entities(Book.accessionNo,Book.title).filter(Book.accessionNo == accessionid).first()
        local_session.close()
        return (True,{ 'memberid' : m.memberID, 'name' : m.name, 'bookid': b.accessionNo, 'title' : b.title, 'bdate' : datetime.now().date(),  'ddate' : duedate})
    except:
        local_session.close()
        return (False,'Missing or incomplete fields')
def info1(accessionid,dat):
    try:
        dat = datetime.strptime(dat + f' {datetime.now().time().replace(microsecond=0)}', '%Y-%m-%d %H:%M:%S')
        local_session = session(bind = engine)
        b = local_session.query(BookLoan).with_entities(BookLoan.accessionNo, BookLoan.memberID).filter(BookLoan.accessionNo == accessionid).first()
        if b != []:
            m = local_session.query(Membership).with_entities(Membership.memberID,Membership.name).filter(Membership.memberID == b.memberID).first()
            bb = local_session.query(Book).with_entities(Book.accessionNo,Book.title).filter(Book.accessionNo == b.accessionid).first()
            local_session.close()
            return (True, {'memberid' : m.memberID, 'name' : m.name, 'bookid': bb.accessionNo, 'title' : bb.title, 'rdate' : f'{dat.date()}'})
        else:
            local_session.close()
            return (False, 'Book not borrowed')
    except:
        local_session.close()
        return (False, 'Missing or incomplete fields')

def info2(accessionid, memberid):
    try:
        local_session = session(bind = engine)
        m = local_session.query(Membership).with_entities(Membership.memberID,Membership.name).filter(Membership.memberID == memberid).first()
        b = local_session.query(Book).with_entities(Book.accessionNo,Book.title).filter(Book.accessionNo == accessionid).first()
        local_session.close()
        return (True,[m.memberID,m.name,b.accessionNo,b.title])
    except:
        local_session.close()
        return(False, "Missing or in complete fields")

        




def borrow(accessionid, memberid):
    try:
        if havefine(memberid,datetime.now().strftime("%Y-%m-%d")):
            return (False,'Access denied pay fine')
        if isborrow(accessionid):
            a = select(*BookLoan.__table__.columns).where(BookLoan.accessionNo == accessionid)
            local_session = session(bind = engine)
            a = local_session.execute(a).first()
            duedate = a[1].date() + timedelta(14)
            local_session.close()
            return (False,f"Access denied book on loan until {duedate}")
        if not canborrow(memberid):
            return "borrow two books"
        if isreserve(accessionid, memberid) == "cannot borrow":
            return (False,'Access denied book on reservation')
        else:
            if isreserve(accessionid, memberid) == "yes":
                local_session = session(bind = engine) #datetime.strptime(d + f' {datetime.now().time().replace(microsecond=0)}', '%Y-%m-%d %H:%M:%S')
                new_loan = BookLoan(accessionNo = accessionid, borrowDate = datetime.now(),memberID = memberid)
                local_session.add(new_loan)
                local_session.query(BookReservation).filter(and_(BookReservation.accessionNo == accessionid, BookReservation.memberID == memberid)).delete()
                local_session.commit()
                local_session.close()
                return (True,)
            else:
                local_session = session(bind = engine)
                new_loan = BookLoan(accessionNo = accessionid, borrowDate = datetime.now() , memberID = memberid)
                local_session.add(new_loan)
                #local_session.query(Book).filter(Book.accessionNo == accessionid).one().memberID = memberid
                local_session.query(BookReservation).filter(and_(BookReservation.accessionNo == accessionid, BookReservation.memberID == memberid)).delete()
                local_session.commit()
                local_session.close()
                return (True,)
    except:
        return (False,'Acess denied invalid input')

def returning(accessionid, datereturn):
    local_session = session(bind = engine)
    a = select(*BookLoan.__table__.columns).where(BookLoan.accessionNo == accessionid)
    a = local_session.execute(a).first()
    dat = datetime.strptime(datereturn + f' {datetime.now().time().replace(microsecond=0)}', '%Y-%m-%d %H:%M:%S')
    if a:
        m = (dat.date() - a[1].date()).days - 14
        if m > 0:
            fin = local_session.query(Fine).with_entities(Fine.amount).filter(Fine.memberID == a[2]).first()
            local_session.query(Fine).filter(Fine.memberID == a[2]).update({'amount' : fin.amount + m})
        local_session.query(BookLoan).filter(and_(BookLoan.accessionNo == accessionid)).delete()
        if isreserve(accessionid, a[2]) == 'borrow':
            local_session.quert(BookReservation).filter(and_(BookReservation.accessionNo == accessionid, BookReservation.memberID == a[2])).delete()
        local_session.commit()
        local_session.close()
        return (True, "Book returned")
    local_session.close()
    return (False, "Book not borrowed")



def fine(memberid, paymentdate, paymentamt):
    dat = datetime.strptime(paymentdate + f' {datetime.now().time().replace(microsecond=0)}', '%Y-%m-%d %H:%M:%S')
    if not havefine(memberid,paymentdate):
        return (False, 'No Fine')
    if not getfineamt(memberid,paymentdate):
        return (False, "Please return due book")
    else:
        if paymentamt == getfineamt(memberid,paymentdate):
            local_session = session(bind = engine)
            dat = datetime.strptime(paymentdate + f' {datetime.now().time().replace(microsecond=0)}', '%Y-%m-%d %H:%M:%S')
            local_session.query(Fine).filter(Fine.memberID == memberid).update( {'paymentDate' : dat, 'amount' : 0 })
            local_session.commit()
            local_session.close()
            return (True, "Fine Paid")
        else:
            return (False, "Wrong Amount")


def memberwithfine():
    local_session = session(bind = engine)
    
    l =[]
    for i in local_session.query(Membership):
        l1 = []
        if havefine(f'{i}',datetime.now().strftime("%Y-%m-%d")):
            for i1 in local_session.query(Membership).with_entities(Membership.memberID,Membership.name,Membership.telNo,Membership.faculty,Membership.eMail).filter(Membership.memberID == f'{i}').first():
                l1.append(i1)
            l.append(l1)
    local_session.close()
    return l


def reserve(accessionid, memberid, reservedate):
    local_session = session(bind = engine)
    try:
        if isreserve(accessionid, memberid) != 'yes':
            return (False, 'Book is reserve')
        if not isborrow(accessionid):
            return (False, 'Book is not on loan')
        if not (reservecount(memberid)):
            return (False, "Reservation limit reached")
        if hasfine(memberid):
            return (False, "Please pay fine")
        local_session = session(bind = engine)
        a = select(*BookReservation.__table__.columns).where(and_(BookReservation.accessionNo == accessionid, BookReservation.memberID == memberid))
        a = local_session.execute(a).first()
        if a:
            local_session.close()
            return (False, "You have already reserve the book")
        else:
            dat = datetime.datetime.strptime(reservedate , '%Y-%m-%d').date()
            local_session.add(BookReservation(accessionNo = accessionid, reserveDate = dat, memberID = memberid))
            local_session.commit()
            local_session.close()
            return (True,'Success')
    except:
        return (False,'Wrong entry')

print(reserve("A01","A101A",'2009-09-09'))
print(reserve('A01','A201B','2022-09-09'))
def deletereserve(accessionid, memberid, canceldate):
    if isreserve(accessionid, memberid) == 'borrow' and isborrow(accessionid):
        local_session = session(bind = engine)
        local_session.query(BookReservation).filter(and_(BookReservation.accessionNo == accessionid, BookReservation.memberID == memberid)).delete()
        local_session.commit()
        local_session.close()
        return True
    return False
