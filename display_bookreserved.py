import pymysql
from datetime import date



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
def display_bookreserved():
    con = create_connection()
    cursor = con.cursor()
    find_bookreserved = ("SELECT b.accessionNo, b.title, m.memberID, m.name FROM Membership m, Book b, Bookreservation br WHERE m.memberID  = br.memberID AND b.accessionNo = br.accessionNo")
    cursor.execute(find_bookreserved)

    result = cursor.fetchall()
    for row in result:
        print(row)
        print("\n") 
    return result

display_bookreserved()
