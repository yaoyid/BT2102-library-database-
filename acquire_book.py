import pymysql
from datetime import date




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

def acquire_book(id, title, isbn, publisher, year, *authors):
    con = create_connection()
    cursor = con.cursor()
    book = (id, title, isbn, publisher, year)
    acquire = ("INSERT INTO Book "
               "(accessionNo, title, isbn, publisher, yearPublished) "
               "VALUES (%s, %s, %s, %s, %s)") 
    cursor.execute(acquire, book)

    con.commit()
    con.close()
    con = create_connection()
    cursor = con.cursor()
    add_author = ("INSERT INTO Author "
               "(accessionNo, name) "
               "VALUES (%s, %s)")
    for author in authors:
        author_detail = (id, author)
        cursor.execute(add_author, author_detail)
    con.commit()
    con.close()

#acquire_book('3','book', '2123','se','2000', 's','d')
