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

def create_member(id, name, telNo, faculty, email):
    con = create_connection()
    cursor = con.cursor()
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

#create_member('007','23','2333', '23333', '233@')
