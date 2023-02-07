import pymysql
from datetime import date

from pymysql import NULL



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

def member_getName(id):
    con = create_connection()
    cursor = con.cursor()
    query = "SELECT name From Membership WHERE memberID = %s"
    cursor.execute(query,id)
    result = cursor.fetchall()
    return result

def borrow_getName(accessionNo):
    con = create_connection()
    cursor = con.cursor()
    query = "SELECT name From Membership WHERE memberID = (SELECT memberID FROM BookLoan WHERE accessionNo = %s)"
    cursor.execute(query,accessionNo)
    result = cursor.fetchall()
    return result

borrow_getName('A05')

def borrow_getID(accessionNo):
    con = create_connection()
    cursor = con.cursor()
    query = "SELECT memberID FROM BookLoan WHERE accessionNo = %s"
    cursor.execute(query,accessionNo)
    result = cursor.fetchall()
    return result
borrow_getID('A05')

def borrow_getDue(accessionNo):
    con = create_connection()
    cursor = con.cursor()
    query = "SELECT dueDate FROM BookLoan WHERE accessionNo = %s"
    cursor.execute(query,accessionNo)
    result = cursor.fetchall()
    return result
borrow_getDue('A05')


def book_search(word,field):
    con = create_connection()
    cursor = con.cursor()
    query_book = ""
    search = word
    if field == "Author" or 'author':
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Author WHERE LOWER(name) LIKE %s OR LOWER(name) LIKE %s OR LOWER(name) LIKE %s OR LOWER(name) LIKE %s);"
        search = (word, word + " %", "% " + word, "% " + word + " %")
    if field =="yearPublished":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE yearPublished = %s);"
        search = (word)
    if field == "isbn":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE isbn = %s);"
        search = (word)
    if field =="publisher":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE LOWER(publisher) LIKE %s OR LOWER(publisher) LIKE %s OR LOWER(publisher) LIKE %s OR LOWER(publisher) LIKE %s);"
        search = (word, word + " %", "% " + word, "% " + word + " %")
    if field =="title":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM Book WHERE LOWER(title) LIKE %s OR LOWER(title) LIKE %s OR LOWER(title) LIKE %s OR LOWER(title) LIKE %s);"
        search = (word, word + " %", "% " + word, "% " + word + " %")
    if field == "accessionNo":
        query_book = "SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo = %s;"
        search = (word)
    cursor.execute(query_book,search)
    result = cursor.fetchall()
    con.close()
    return result
book_search('a', 'title')
member_getName("007")[0]['name']

con = pymysql.connect(host="localhost", user="root", password="Duanyaoyi1209", db="ALibrarySystem", cursorclass=pymysql.cursors.DictCursor)
with con.cursor() as cur:
        cur.execute("SELECT * FROM Membership where memberID = %s", ("A101A"))
res = cur.fetchall()


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
    con.close()
    return result
