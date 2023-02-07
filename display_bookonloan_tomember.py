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
cursor = con.cursor()
def display_bookonloan_tomember(id):
    con = create_connection()
    cursor = con.cursor()
    find_bookonloan_tomember = ("SELECT b.*, (SELECT GROUP_CONCAT(a.name SEPARATOR ',')  FROM Author a WHERE b.accessionNO = a.accessionNo) as author_name FROM Book b WHERE b.accessionNo IN (SELECT accessionNo FROM BookLoan WHERE memberID = %s);")
    cursor.execute(find_bookonloan_tomember, id)
    result = cursor.fetchall()
    for row in result:
        print(row)
        print("\n") 
    return result

display_bookonloan_tomember("A201B")
