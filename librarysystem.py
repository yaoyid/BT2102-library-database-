from decimal import Decimal
from sqlalchemy import ForeignKey, create_engine, false
from sqlalchemy import Column, String, Integer, DateTime, BOOLEAN, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
import pymysql
import mysql.connector
from sqlalchemy.sql import func

#db = mysql.connector.connect(user = "root",passwd="********", host ="127.0.0.1", port = 3306,database = "ALS")
#cursor = db.cursor()
#cursor.execute("select * from book")
#for i in cursor:
#    print(i)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
#///?User=root&;Password=********&Host=127.0.0.1&Port=3306&Database=ALS'
engine = create_engine('mysql+pymysql://root:Duanyaoyi1209@127.0.0.1/ALibrarySystem',echo=True)
base = declarative_base() 
session = sessionmaker()

class Membership(base):
    __tablename__= 'Membership'
    memberID = Column(String(10), primary_key= True)
    name = Column(String(25), nullable= False)
    faculty = Column(String(15), nullable= False)
    telNo = Column(String(15), nullable = False)
    eMail = Column(String(25), nullable = False)

    def __repr__(self):
        return f"{self.memberID}"

class Book(base):
    __tablename__= 'Book'
    accessionNo = Column(String(10), primary_key= True)
    title = Column(String(100), nullable= False)
    isbn = Column(String(15), nullable= False)
    publisher = Column(String(100), nullable = False)
    yearPublished = Column(Integer(), nullable = False)
    def __repr__(self):
        return f"{self.accessionNo}"

class Author(base):
    __tablename__= 'Author'
    accessionNo = Column(String(10), ForeignKey('Book.accessionNo'), primary_key= True)
    name = Column(String(100), primary_key= True)

    def __repr__(self):
        return f"{self.name}"

class Fine(base):
    __tablename__= 'Fine'
    memberID = Column(String(10), ForeignKey('Membership.memberID'), primary_key= True)
    paymentDate = Column(DateTime(), nullable = True)
    amount = Column(Integer(), nullable= False)

    def __repr__(self):
        return f"{self.memberID}"


class BookLoan(base):
    __tablename__ = "BookLoan"
    accessionNo = Column(ForeignKey(Book.accessionNo), primary_key= True)
    borrowDate = Column(DateTime(), nullable = False, primary_key= False)
    dueDate = Column(DateTime(), nullable = False)
    memberID = Column(ForeignKey(Membership.memberID), primary_key= True)

class BookReservation(base):
    __tablename__ = "BookReservation"
    accessionNo = Column(ForeignKey(Book.accessionNo), primary_key= True)
    reserveDate= Column(DateTime(), nullable = False)
    memberID = Column(ForeignKey(Membership.memberID), primary_key= True)
