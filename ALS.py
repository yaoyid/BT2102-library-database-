import pymysql
from tkinter import *
from tkinter import messagebox
from datetime import *
from NEWADD import *
from addMember import *
from sqlalchemy import false
from fine_payment import *
from book_search import *
from borrow_reserve import *
from tkinter import messagebox
from tkinter import ttk
from return_book import update_fine
from acquire_book import *
from ast import excepthandler
from tkinter import messagebox
from numpy import delete
from delete_reserve import *
from book_withdraw import *
import display_loan
import display_bookonloan_tomember
import display_bookreserved
import display_fine

root = Tk()
def start():
    MenuW()
startButton = Button(root, text = "Start", command = start)
startButton.pack()

def MenuW():
    global mainMenu
    mainMenu = Toplevel()
    mainMenu.title("Library")
    mainMenu.geometry('1280x720')
    headerLabel = Label(mainMenu, text = "Library",
                    bg = "lightblue", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    bookSearchButton = Button(mainMenu, text = "Membership",
                       font = ("lucida", 18 ), command = lambda : [membershipMenuW(),mainMenu.destroy()])
    bookSearchButton.place(x = 390, y = 150, width = 500, height = 60)

    booksOnLoanButton = Button(mainMenu, text = "Books",
                        font = ("lucida", 18), command = lambda :[booksMenuW(),mainMenu.destroy()])
    booksOnLoanButton.place(x = 390, y = 250, width = 500, height = 60)

    booksOnReservationButton = Button(mainMenu, text = "Loans",
                        font = ("lucida", 18), command = lambda :[loansMenuW(),mainMenu.destroy()])
    booksOnReservationButton.place(x = 390, y = 350, width = 500, height = 60)

    outstandingFinesButton = Button(mainMenu, text = "Reservations",
                        font = ("lucida", 18), command = lambda :[reservationMenuW(),mainMenu.destroy()])
    outstandingFinesButton.place(x = 390, y = 450, width = 500, height = 60)

    booksOnLoanToMemberButton = Button(mainMenu, text = "Fines",
                        font = ("lucida", 18), command = lambda :[finesMenuW(),mainMenu.destroy()])
    booksOnLoanToMemberButton.place(x = 390, y = 550, width = 500, height = 60)

    backButton = Button(mainMenu, text = 'Reports',
                    font = ("lucida", 18), command= lambda :[reportsMenuW(),mainMenu.destroy()])
    backButton.place(x = 390, y = 650, width = 500, height = 50)






def membershipMenuW(): 
    global membershipMenu
    membershipMenu = Toplevel()
    membershipMenu.title("Membership")
    membershipMenu.geometry("1280x720")

    def membershipMainToCreate():
        membershipCreateW()
        membershipMenu.destroy()
    
    def membershipMainToDelete():
        membershipDeleteW()
        membershipMenu.destroy()

    def membershipMainToUpdate():
        membershipUpdateMenuW()
        membershipMenu.destroy()
    
    def membershipToMain():
        pass
         
    headerLabel = Label(membershipMenu, text = "Select One of the Options Below:",
                        bg = "lightblue", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    creationButton = Button(membershipMenu, text = "Membership Creation", command = membershipMainToCreate, font = ("lucida", 18 ))
    creationButton.place(x = 390, y = 150, width = 500, height = 60)

    deletionButton = Button(membershipMenu, text = "Membership Deletion", command = membershipMainToDelete, font = ("lucida", 18))
    deletionButton.place(x = 390, y = 250, width = 500, height = 60)

    updateButton = Button(membershipMenu, text = "Membership Update", command = membershipMainToUpdate, font = ("lucida", 18))
    updateButton.place(x = 390, y = 350, width = 500, height = 60)

    backToMainButton = Button(membershipMenu, text = "Back To Main Menu", command = lambda : [MenuW(),membershipMenu.destroy()],
                        font = ("lucida", 16))
    backToMainButton.place(x = 160, y = 600, width = 960, height = 50)

def membershipCreateW():
    global membershipCreation
    membershipCreation = Toplevel()
    membershipCreation.title("Membership - Creation")
    membershipCreation.geometry("1280x720")

    def membershipCreateToMember():
        membershipMenuW()
        membershipCreation.destroy()

    def create_member():
        try:
            member_id = memberID.get()
            member_name = name.get()
            fac = faculty.get()
            telNo = phone.get()
            email = emailAddress.get()           
        except:
            membershipIncompleteEW()
        con = pymysql.connect(host="localhost", user="root",  password = "Duanyaoyi1209", db="ALibrarySystem", cursorclass=pymysql.cursors.DictCursor)
        with con.cursor() as cur:
            cur.execute("SELECT * FROM Membership where memberID = %s", (member_id))
            result = cur.fetchall()
            if len(result) > 0:
                memberExistEW()
            else:
                cur.execute('INSERT INTO Membership VALUES (%s, %s, %s, %s, %s)', 
                (member_id, member_name, fac, str(telNo), email)) 
                con.commit()

                cur.execute('INSERT INTO Fine VALUES (%s, %s, %s)', 
                (member_id, date.today(), 0)) 
                con.commit()
                membershipCreateSuccessW()
            con.close()
    
    def memberExistEW():
        global membershipExistE
        membershipExistE = Toplevel()
        membershipExistE.title("Membership Creation Error")
        membershipExistE.geometry("300x300")
        membershipExistE.configure(bg = "red")

        headerLabel = Label(membershipExistE, text = "Error!", font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(membershipExistE, text = "Member already exists.", font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(membershipExistE, text = "Back to Create Function", font = ("lucida", 15), wraplength = 150, command=membershipExistE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
    
    def membershipIncompleteEW():
        global membershipIncompleteE
        membershipIncompleteE = Toplevel()
        membershipIncompleteE.title("Membership Creation Error")
        membershipIncompleteE.geometry("300x300")
        membershipIncompleteE.configure(bg = "red")

        headerLabel = Label(membershipIncompleteE, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(membershipIncompleteE, text = "Missing or Incomplete fields.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(membershipIncompleteE, text = "Back to Create Function", font = ("lucida", 15), wraplength = 150, command = membershipIncompleteE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
    
    def membershipCreateSuccessW():
        global membershipCreateSuccess
        membershipCreateSuccess = Toplevel()
        membershipCreateSuccess.title("Membership Creation Success")
        membershipCreateSuccess.geometry("300x300")
        membershipCreateSuccess.configure(bg = "SpringGreen3")

        headerLabel = Label(membershipCreateSuccess, text = "Sucess!", font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "SpringGreen3")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "black")

        middleLabel = Label(membershipCreateSuccess, text = "ALS Membership Created.", font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "SpringGreen3")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "black")

        backButton = Button(membershipCreateSuccess, text = "Back to Create Function", font = ("lucida", 15), wraplength = 150, command=membershipCreateSuccess.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
        

    headerLabel = Label(membershipCreation, text = "To Create Member, Please Enter Requested Information Below:",
                        bg = "turquoise", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)
    
    memberIDLabel = Label(membershipCreation, text = "Membership ID: ", font = ("lucida", 18))
    memberIDLabel.place(x = 300, y = 125, width = 170, height = 50)
    memberID = StringVar()
    memberIDEntry = Entry(membershipCreation, textvariable = memberID)
    memberIDEntry.place(x = 470, y = 125, width = 510, height = 50)

    nameLabel = Label(membershipCreation, text = "Name: ", font = ("lucida", 18))
    nameLabel.place(x = 300, y = 200, width = 170, height = 50)
    name = StringVar()
    nameEntry = Entry(membershipCreation, textvariable = name)
    nameEntry.place(x = 470, y = 200, width = 510, height = 50)

    facultyLabel = Label(membershipCreation, text = "Faculty: ", font = ("lucida", 18))
    facultyLabel.place(x = 300, y = 275, width = 170, height = 50)
    faculty = StringVar()
    facultyEntry = Entry(membershipCreation, textvariable = faculty)
    facultyEntry.place(x = 470, y = 275, width = 510, height = 50)

    phoneLabel = Label(membershipCreation, text = "Phone Number: ", font = ("lucida", 18))
    phoneLabel.place(x = 300, y = 350, width = 170, height = 50)
    phone = IntVar()
    phoneEntry = Entry(membershipCreation, textvariable = phone)
    phoneEntry.place(x = 470, y = 350, width = 510, height = 50)
    phoneEntry.delete(0, END)

    emailLabel = Label(membershipCreation, text = "Email Address: ", font = ("lucida", 18))
    emailLabel.place(x = 300, y = 425, width = 170, height = 50)
    emailAddress = StringVar()
    emailEntry = Entry(membershipCreation, textvariable = emailAddress)
    emailEntry.place(x = 470, y = 425, width = 510, height = 50)

    createButton = Button(membershipCreation, text = "Create Member", font = ("lucida", 20), command = create_member)
    createButton.place(x = 375, y = 575, width = 225, height = 80)

    backButton = Button(membershipCreation, text = "Back To Membership Menu", font = ("lucida", 18), command=membershipCreateToMember)
    backButton.place(x = 705, y = 575, width = 225, height = 80)

def membershipDeleteW():
    global membershipDeletion
    membershipDeletion = Toplevel()
    membershipDeletion.title("Membershp - Deletion")
    membershipDeletion.geometry("1280x720")

    def membershipDeleteToMenu():
        membershipMenuW()
        membershipDeletion.destroy()
    
    def membershipDeleteValidate(member_ID):
        if hasloan(member_ID) or has_reservation(member_ID) or hasfine(member_ID):
            memberDeleteEW()
        else:
            memberDeleteConfirmW(member_ID)
    
    def memberDeleteEW():
        global memberDeleteE
        memberDeleteE = Toplevel()
        memberDeleteE.title("Membership Deletion Error")
        memberDeleteE.geometry("300x300")
        memberDeleteE.configure(bg = "red")

        headerLabel = Label(memberDeleteE, text = "Error!", font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(memberDeleteE, text = "Member has loans,\n reservations or outstanding fines.", font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(memberDeleteE, text = "Back to Create Function", font = ("lucida", 15), wraplength = 150, command = memberDeleteE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
    def Deleted():
        global Deleted
        Deleted = Toplevel()
        Deleted.title("Membership Deletion ")
        Deleted.geometry("300x300")
        Deleted.configure(bg = "SpringGreen3")

        middleLabel = Label(Deleted, text = "Member deleted", font = ("lucida", 15), borderwidth = 3, wraplength = 200)
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)


        backButton = Button(Deleted, text = "Back to Create Function", font = ("lucida", 15), wraplength = 150, command = Deleted.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
    
    def memberDeleteConfirmW(member_ID):
        global memberDeleteConfirm
        memberDeleteConfirm = Toplevel()
        memberDeleteConfirm.title("Confirm Deletion")
        memberDeleteConfirm.geometry("350x450")
        memberDeleteConfirm.configure(bg = "SpringGreen3")
        con = pymysql.connect(host="localhost", user="root", password="Duanyaoyi1209", db="ALibrarySystem", cursorclass=pymysql.cursors.DictCursor)
        with con.cursor() as cur:
            cur.execute("SELECT * FROM Membership where memberID = %s", (member_ID))
        res = cur.fetchall()
        
        def delete_member(member_ID):
            con = pymysql.connect(host="localhost", user="root", password="Duanyaoyi1209", db="ALibrarySystem", cursorclass=pymysql.cursors.DictCursor) 
            with con.cursor() as cur:
                cur.execute("DELETE FROM Membership WHERE memberID = %s", member_ID)
                con.commit()
            con.close()
            Deleted()

        headerLabel = Label(memberDeleteConfirm, text = "Please Confirm Details To\n Be Correct",
                            font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
        headerLabel.place(x = 25, y = 0, width = 300, height = 100)

       

        memberIDLabel = Label(memberDeleteConfirm, text = "Member ID: " + member_ID,
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberIDLabel.place(x = 25, y = 100, width = 300, height = 50)

        memberNameLabel = Label(memberDeleteConfirm, text = "Name: " + res[0]['name'],
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberNameLabel.place(x = 25, y = 150, width = 300, height = 50)

        memberFacLabel = Label(memberDeleteConfirm, text = "Faculty: " + res[0]['faculty'],
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberFacLabel.place(x = 25, y = 200, width = 300, height = 50)

        memberPhoneLabel = Label(memberDeleteConfirm, text = "Phone Number: " + res[0]['telNo'],
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberPhoneLabel.place(x = 25, y = 250, width = 300, height = 50)

        memberEmailLabel = Label(memberDeleteConfirm, text = "Email Address: " + res[0]['eMail'],
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberEmailLabel.place(x = 25, y = 300, width = 300, height = 50)

        confirmButton = Button(memberDeleteConfirm, text = "Confirm Deletion",
                            font = ("lucida", 15), wraplength = 100, command = lambda: delete_member(member_ID))
        confirmButton.place(x = 50, y = 375, width = 100, height = 50)

        backButton = Button(memberDeleteConfirm, text = "Back to Delete Function",
                            font = ("lucida", 15), wraplength = 100, command=memberDeleteConfirm.destroy)
        backButton.place(x = 200, y = 375, width = 100, height = 50)

    headerLabel = Label(membershipDeletion, text = "To Delete Member, Please Enter Membership ID: ",
                        bg = "turquoise", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    memberIDLabel = Label(membershipDeletion, text = "Membership ID: ", font = ("lucida", 18))
    memberIDLabel.place(x = 300, y = 275, width = 170, height = 50)
    memberID = StringVar()
    memberIDEntry = Entry(membershipDeletion, textvariable = memberID)
    memberIDEntry.place(x = 470, y = 275, width = 510, height = 50)

    deleteButton = Button(membershipDeletion, text = "Delete Member", font = ("lucida", 20), command = lambda: membershipDeleteValidate(memberID.get()))
    deleteButton.place(x = 375, y = 575, width = 225, height = 80)

    backToMembershipButton = Button(membershipDeletion, text = "Back To\n Membership Menu", font = ("lucida", 20), command = membershipDeleteToMenu)
    backToMembershipButton.place(x = 705, y = 575, width = 225, height = 80)

def membershipUpdateMenuW():
    global membershipUpdateMenu
    membershipUpdateMenu = Toplevel()
    membershipUpdateMenu.title("Membership - Update")
    membershipUpdateMenu.geometry("1280x720")

    def membershipUpdateMenuToInfo(memberID):
        con = pymysql.connect(host="localhost", user="root", password="Duanyaoyi1209", db="ALibrarySystem", cursorclass=pymysql.cursors.DictCursor)
        with con.cursor() as cur:
            cur.execute("SELECT * FROM Membership where memberID = %s", (memberID))
            result = cur.fetchall()
        if len(result) == 0:
            membershipUpdateExistEW()
        else:
            membershipUpdateInfoW(memberID)
            membershipUpdateMenu.destroy()
    
    def membershipUpdateToMenu():
        membershipMenuW()
        membershipUpdateMenu.destroy()
    
    def membershipUpdateExistEW():
        global membershipUpdateExistE
        membershipUpdateExistE = Toplevel()
        membershipUpdateExistE.title("Membership Update Error")
        membershipUpdateExistE.geometry("300x300")
        membershipUpdateExistE.configure(bg = "red")

        headerLabel = Label(membershipUpdateExistE, text = "Error!", font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(membershipUpdateExistE, text = "Member does not exist.", font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(membershipUpdateExistE, text = "Back to Update Function", font = ("lucida", 15), wraplength = 150, command=membershipUpdateExistE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)


    headerLabel = Label(membershipUpdateMenu, text = "To Update a Member, Please Enter Membership ID: ",
                        bg = "turquoise", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    memberIDLabel = Label(membershipUpdateMenu, text = "Membership ID: ", font = ("lucida", 18))
    memberIDLabel.place(x = 300, y = 275, width = 170, height = 50)
    memberID = StringVar()
    memberIDEntry = Entry(membershipUpdateMenu, textvariable = memberID)
    memberIDEntry.place(x = 470, y = 275, width = 510, height = 50)

    updateButton = Button(membershipUpdateMenu, text = "Update Member", font = ("lucida", 20), command =lambda: membershipUpdateMenuToInfo(memberID.get()))
    updateButton.place(x = 375, y = 575, width = 225, height = 80)

    backToMembershipButton = Button(membershipUpdateMenu, text = "Back To\n Membership Menu", font = ("lucida", 20), command = membershipUpdateToMenu)
    backToMembershipButton.place(x = 705, y = 575, width = 225, height = 80)

def membershipUpdateInfoW(member_ID):
    global membershipUpdateInfo
    membershipUpdateInfo = Toplevel()
    membershipUpdateInfo.title("Membership - Update")
    membershipUpdateInfo.geometry("1280x720")

    def membershipUpdateInfoToMenu():
        membershipMenuW()
        membershipUpdateInfo.destroy()
    
    def memberUpdateValidate(): 
        try:
            ##member_ID = memberID.get()
            member_name = name.get()
            member_fac = faculty.get()
            member_phone = phone.get()
            email = emailAddress.get()
        except:
            membershipUpdateEW()
        else:
            memberUpdateConfirmW(member_ID, member_name, member_fac, member_phone, email)
        
    def membershipUpdateEW():
        global membershipUpdateE
        membershipUpdateE = Toplevel()
        membershipUpdateE.title("Membership Update Error")
        membershipUpdateE.geometry("300x300")
        membershipUpdateE.configure(bg = "red")

        headerLabel = Label(membershipUpdateE, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(membershipUpdateE, text = "Missing or Incomplete fields.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(membershipUpdateE, text = "Back to Update Function",
                            font = ("lucida", 15), wraplength = 150, command=membershipUpdateE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)       

    def memberUpdateConfirmW(member_ID, member_name, member_fac, member_phone, email):
        global memberUpdateConfirm
        memberUpdateConfirm = Toplevel()
        memberUpdateConfirm.title("Confirm Update")
        memberUpdateConfirm.geometry("350x450")
        memberUpdateConfirm.configure(bg = "SpringGreen3")

        def update_member(member_ID, member_name, member_fac, member_phone, email):
            memberUpdateConfirm.destroy
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
            
            update_member_name(member_ID, member_name)
            update_member_faculty(member_ID, member_fac)
            update_member_phone(member_ID, member_phone)
            update_member_email(member_ID, email)

            memberUpdateSuccessW()
            return 

        headerLabel = Label(memberUpdateConfirm, text = "Please Confirm Updated Details To Be Correct",
                            font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
        headerLabel.place(x = 25, y = 0, width = 300, height = 100)

        memberIDLabel = Label(memberUpdateConfirm, text = "Member ID: " + member_ID,
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberIDLabel.place(x = 25, y = 100, width = 300, height = 50)

        memberNameLabel = Label(memberUpdateConfirm, text = "Name: " + member_name,
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberNameLabel.place(x = 25, y = 150, width = 300, height = 50)

        memberFacLabel = Label(memberUpdateConfirm, text = "Faculty: " + member_fac,
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberFacLabel.place(x = 25, y = 200, width = 300, height = 50)

        memberPhoneLabel = Label(memberUpdateConfirm, text = "Phone Number: " + str(member_phone),
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberPhoneLabel.place(x = 25, y = 250, width = 300, height = 50)

        memberEmailLabel = Label(memberUpdateConfirm, text = "Email Address: " + email,
                                font = ("lucida", 15), wraplength = 300, bg = "SpringGreen3")
        memberEmailLabel.place(x = 25, y = 300, width = 300, height = 50)

        confirmButton = Button(memberUpdateConfirm, text = "Confirm Update",
                            font = ("lucida", 15), wraplength = 100, command= lambda: update_member(member_ID, member_name, member_fac, member_phone, email))
        confirmButton.place(x = 50, y = 375, width = 100, height = 50)

        backButton = Button(memberUpdateConfirm, text = "Back to Update Function",
                            font = ("lucida", 15), wraplength = 100, command=memberUpdateConfirm.destroy)
        backButton.place(x = 200, y = 375, width = 100, height = 50)
    
    def memberUpdateSuccessW():
        global memberUpdateSuccess
        memberUpdateSuccess = Tk()
        memberUpdateSuccess.title("Membership Update Success")
        memberUpdateSuccess.geometry("300x300")
        memberUpdateSuccess.configure(bg = "SpringGreen3")

        headerLabel = Label(memberUpdateSuccess, text = "Sucess!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "SpringGreen3")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "black")

        middleLabel = Label(memberUpdateSuccess, text = "ALS Membership Updated.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "SpringGreen3")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "black")

        backButton = Button(memberUpdateSuccess, text = "Back to Update Function",
                            font = ("lucida", 15), wraplength = 150, command=memberUpdateSuccess.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)

    headerLabel = Label(membershipUpdateInfo, text = "Please Enter Requested Information Below:",
                        bg = "turquoise", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    con = pymysql.connect(host="localhost", user="root", password="Duanyaoyi1209", db="ALibrarySystem", cursorclass=pymysql.cursors.DictCursor)
    with con.cursor() as cur:
        cur.execute("SELECT * FROM Membership where memberID = %s", (member_ID))
        res = cur.fetchall()

    memberIDLabel = Label(membershipUpdateInfo, text = "Membership ID: ", font = ("lucida", 18))
    memberIDLabel.place(x = 300, y = 125, width = 170, height = 50)
    memberID = StringVar()
    memberIDEntry = Entry(membershipUpdateInfo, textvariable = memberID)
    memberIDEntry.insert(0, member_ID)
    memberIDEntry.configure(state="disable")
    memberIDEntry.place(x = 470, y = 125, width = 510, height = 50)

    nameLabel = Label(membershipUpdateInfo, text = "Name: ", font = ("lucida", 18))
    nameLabel.place(x = 300, y = 200, width = 170, height = 50)
    name = StringVar()
    nameEntry = Entry(membershipUpdateInfo, textvariable = name)
    nameEntry.insert(0, res[0]['name'])
    nameEntry.place(x = 470, y = 200, width = 510, height = 50)

    facultyLabel = Label(membershipUpdateInfo, text = "Faculty: ", font = ("lucida", 18))
    facultyLabel.place(x = 300, y = 275, width = 170, height = 50)
    faculty = StringVar()
    facultyEntry = Entry(membershipUpdateInfo, textvariable = faculty)
    facultyEntry.insert(0, res[0]['faculty'])
    facultyEntry.place(x = 470, y = 275, width = 510, height = 50)

    phoneLabel = Label(membershipUpdateInfo, text = "Phone Number: ", font = ("lucida", 18))
    phoneLabel.place(x = 300, y = 350, width = 170, height = 50)
    phone = IntVar()
    phoneEntry = Entry(membershipUpdateInfo, textvariable = phone)
    phoneEntry.delete(0, END)
    phoneEntry.insert(0, res[0]['telNo'])
    phoneEntry.place(x = 470, y = 350, width = 510, height = 50)

    emailLabel = Label(membershipUpdateInfo, text = "Email Address: ", font = ("lucida", 18))
    emailLabel.place(x = 300, y = 425, width = 170, height = 50)
    emailAddress = StringVar()
    emailEntry = Entry(membershipUpdateInfo, textvariable = emailAddress)
    emailEntry.insert(0, res[0]['eMail'])
    emailEntry.place(x = 470, y = 425, width = 510, height = 50)

    updateButton = Button(membershipUpdateInfo, text = "Update Member", font = ("lucida", 20), command=memberUpdateValidate)
    updateButton.place(x = 375, y = 575, width = 225, height = 80)

    backToMembershipButton = Button(membershipUpdateInfo, text = "Back To\n Membership Menu", font = ("lucida", 20), command = membershipUpdateInfoToMenu)
    backToMembershipButton.place(x = 705, y = 575, width = 225, height = 80)





def booksMenuW():
    global booksMenu
    booksMenu = Toplevel()
    booksMenu.title("Books")
    booksMenu.geometry("1280x720")
    

    def booksMenuToAcquisition():
        booksAcquisitionW()
        booksMenu.destroy()

    def booksMenuToWithdrawal():
        booksWithdrawalW()
        booksMenu.destroy()


    headerLabel = Label(booksMenu, text = "Select One of the Options Below:",
                        bg = "lightblue", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    acquisitionButton = Button(booksMenu, text = "Book Acquisition", font = ("lucida", 18 ), command = booksMenuToAcquisition)
    acquisitionButton.place(x = 390, y = 150, width = 500, height = 60)

    withdrawalButton = Button(booksMenu, text = "Book Withdrawal", font = ("lucida", 18), command = booksMenuToWithdrawal)
    withdrawalButton.place(x = 390, y = 250, width = 500, height = 60)

    backButton = Button(booksMenu, text = "Back To Main Menu", command = lambda : [MenuW(),booksMenu.destroy()],
                        font = ("lucida", 16))
    backButton.place(x = 160, y = 600, width = 960, height = 50)    

def booksAcquisitionW():
    global booksAcquisition
    booksAcquisition = Toplevel()
    booksAcquisition.title("Books - Acquisition")
    booksAcquisition.geometry("1280x720")


    def booksAcquisitionToMenu():
        booksMenuW()
        booksAcquisition.destroy()

    def acquire_book():
        try:
            accession_number = accessionNo.get()
            book_title = title.get()
            book_author = author.get()
            book_isbn = isbn.get()
            book_publisher = publisher.get()
            book_year = year.get()
        except:
            booksAcquisitionEW()
        
        con = pymysql.connect(host='localhost',
            user='root',
            password='Duanyaoyi1209',
            db='ALibrarySystem',
            cursorclass=pymysql.cursors.DictCursor)
        with con.cursor() as cur:
            cur.execute("SELECT * FROM Book where accessionNo = %s", (accession_number))
            result = cur.fetchall()
            if len(result) > 0:
                booksAcquisitionEW()
            else:
                book = (accession_number, book_title, book_isbn, book_publisher, str(book_year))
                cur.execute("INSERT INTO Book VALUES (%s, %s, %s, %s, %s)", book)
                con.commit()
                
                authors = book_author.split(",")
                for name in authors:
                    author_detail = (accession_number, name)
                    cur.execute("INSERT INTO Author VALUES (%s, %s)", author_detail)
                con.commit()
                booksAcquisitionSuccessW()
            con.close()

    def booksAcquisitionEW():
        global booksAcquisitionE
        booksAcquisitionE = Toplevel()
        booksAcquisitionE.title("Book Acquisition Error")
        booksAcquisitionE.geometry("300x300")
        booksAcquisitionE.configure(bg = "red")

        headerLabel = Label(booksAcquisitionE, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(booksAcquisitionE, text = "Book already added;\n Duplicate, Missing or\n Incomplete fields.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(booksAcquisitionE, text = "Back to\n Acquisition\n Function",
                            font = ("lucida", 15), wraplength = 150, command=booksAcquisitionE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
    
    def booksAcquisitionSuccessW():
        global booksAcquisitionSuccess
        booksAcquisitionSuccess = Tk()
        booksAcquisitionSuccess.title("Book Acquisition Success")
        booksAcquisitionSuccess.geometry("300x300")
        booksAcquisitionSuccess.configure(bg = "SpringGreen3")

        headerLabel = Label(booksAcquisitionSuccess, text = "Sucess!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "SpringGreen3")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "black")

        middleLabel = Label(booksAcquisitionSuccess, text = "New Book added in Library.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "SpringGreen3")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "black")

        backButton = Button(booksAcquisitionSuccess, text = "Back to Acquisition Function",
                            font = ("lucida", 15), wraplength = 150, command=booksAcquisitionSuccess.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)


    headerLabel = Label(booksAcquisition, text = "For New Book Acquisition, Please Enter Required Information Below:",
                        font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    accessionNoLabel = Label(booksAcquisition, text = "Accession Number: ", font = ("lucida", 18))
    accessionNoLabel.place(x = 300, y = 125, width = 170, height = 50)
    accessionNo = StringVar()
    accessionNoEntry = Entry(booksAcquisition, textvariable = accessionNo)
    accessionNoEntry.place(x = 470, y = 125, width = 510, height = 50)

    titleLabel = Label(booksAcquisition, text = "Title: ", font = ("lucida", 18))
    titleLabel.place(x = 300, y = 200, width = 170, height = 50)
    title = StringVar()
    titleEntry = Entry(booksAcquisition, textvariable = title)
    titleEntry.place(x = 470, y = 200, width = 510, height = 50)

    authorLabel = Label(booksAcquisition, text = "Author: ", font = ("lucida", 18))
    authorLabel.place(x = 300, y = 275, width = 170, height = 50)
    author = StringVar()
    authorEntry = Entry(booksAcquisition, textvariable = author)
    authorEntry.place(x = 470, y = 275, width = 510, height = 50)

    isbnLabel = Label(booksAcquisition, text = "ISBN: ", font = ("lucida", 18))
    isbnLabel.place(x = 300, y = 350, width = 170, height = 50)
    isbn = StringVar()
    isbnEntry = Entry(booksAcquisition, textvariable = isbn)
    isbnEntry.place(x = 470, y = 350, width = 510, height = 50)
    isbnEntry.delete(0, END)

    publisherLabel = Label(booksAcquisition, text = "Publisher: ", font = ("lucida", 18))
    publisherLabel.place(x = 300, y = 425, width = 170, height = 50)
    publisher = StringVar()
    publisherEntry = Entry(booksAcquisition, textvariable = publisher)
    publisherEntry.place(x = 470, y = 425, width = 510, height = 50)

    yearLabel = Label(booksAcquisition, text = "Publication Year: ", font = ("lucida", 18))
    yearLabel.place(x = 300, y = 500, width = 170, height = 50)
    year = IntVar()
    yearEntry = Entry(booksAcquisition, textvariable = year)
    yearEntry.place(x = 470, y = 500, width = 510, height = 50)
    yearEntry.delete(0, END)

    addButton = Button(booksAcquisition, text = "Add New Book", font = ("lucida", 20), command = acquire_book)
    addButton.place(x = 375, y = 575, width = 225, height = 80)

    backToBooksButton = Button(booksAcquisition, text = "Back To Books Menu", font = ("lucida", 20), command = booksAcquisitionToMenu)
    backToBooksButton.place(x = 705, y = 575, width = 225, height = 80)

def booksWithdrawalW():
    global booksWithdrawal
    booksWithdrawal = Toplevel()
    booksWithdrawal.title("Books - Withdrawal")
    booksWithdrawal.geometry("1280x720")

    def withdrawal():
        try:
            a = accessionNo.get()
        except:
            NErrorW("Missing or Incomplete fields.")
        if a == "":
            NErrorW("Missing or Incomplete fields.")
        else:
            if validatedeletebook(a)[0]:
                confirmWithdrawalW(a)
            else:
                NErrorW(validatedeletebook(a)[1])

    def booksWithdrawalToMenu():
        booksMenuW()
        booksWithdrawal.destroy()

    headerLabel = Label(booksWithdrawal, text = "To Remove Outdated Books from System, Please Enter Required Informatin Below: ",
                        font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    accessionNoLabel = Label(booksWithdrawal, text = "Accession Number: ", font = ("lucida", 18))
    accessionNoLabel.place(x = 300, y = 275, width = 170, height = 50)
    accessionNo = StringVar()
    accessionNoEntry = Entry(booksWithdrawal, textvariable = accessionNo)
    accessionNoEntry.place(x = 470, y = 275, width = 510, height = 50)

    withdrawButton = Button(booksWithdrawal, text = "Withdraw Book", font = ("lucida", 20), command = withdrawal)
    withdrawButton.place(x = 375, y = 575, width = 225, height = 80)

    backToBooksButton = Button(booksWithdrawal, text = "Back To Books Menu", font = ("lucida", 20), command = booksWithdrawalToMenu)
    backToBooksButton.place(x = 705, y = 575, width = 225, height = 80)

def confirmWithdrawalW(a):
    global confirmWithdrawal
    confirmWithdrawal = Toplevel()
    confirmWithdrawal.title("Confirm Withdrawal")
    confirmWithdrawal.geometry('350x450')
    confirmWithdrawal.configure(bg = "SpringGreen3")

    def withdraw_book(accessionid):
        confirmWithdrawal.destroy
        deletebook(accessionid)
        booksWithdrawalSuccessW()

    def backTowithdraw():
        confirmWithdrawal.destroy()
    
    def booksWithdrawalSuccessW():
        global booksWithdrawalSuccess
        booksWithdrawalSuccess = Tk()
        booksWithdrawalSuccess.title("Book Acquisition Success")
        booksWithdrawalSuccess.geometry("300x300")
        booksWithdrawalSuccess.configure(bg = "SpringGreen3")

        headerLabel = Label(booksWithdrawalSuccess, text = "Sucess!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "SpringGreen3")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "black")

        middleLabel = Label(booksWithdrawalSuccess, text = "Book Removed from Library.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "SpringGreen3")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "black")

        backButton = Button(booksWithdrawalSuccess, text = "Back to Withdrawal Function",
                            font = ("lucida", 15), wraplength = 150, command=booksWithdrawalSuccess.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)

    aa = book_search(a,'accessionNo')[0]
    headerLabel = Label(confirmWithdrawal, text = "Please Confirm Details To Be Correct",
                    font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
    headerLabel.place(x = 25, y = 0, width = 300, height = 100)

    AccessionLabel = Label(confirmWithdrawal,text = "Accession Number",
                             font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    AccessionLabel.place(x = 25, y = 50, width = 150, height = 50)
    
    AccessionEntryLabel = Label(confirmWithdrawal,text = aa['accessionNo'],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    AccessionEntryLabel.place(x = 175, y = 50, width = 150, height = 50)

    titleLabel = Label(confirmWithdrawal, text = "Title",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    titleLabel.place(x = 25, y = 100, width = 100, height = 50)

    titleEntryLable = Label(confirmWithdrawal, text = aa['title'], font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    titleEntryLable.place(x = 175, y = 100, width= 150, height = 50)

    isbnLabel = Label(confirmWithdrawal, text = "isbn",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    isbnLabel.place(x = 25, y = 150, width = 150, height = 50)
    isbnEntryLabel = Label(confirmWithdrawal, text = aa['isbn'],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    isbnEntryLabel.place(x = 175, y = 150, width = 150, height = 50)

    publisherLabel = Label(confirmWithdrawal, text = "Publisher",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    publisherLabel.place(x = 25, y = 200, width = 150, height = 50)
    publisherEntryLabel = Label(confirmWithdrawal, text = aa['publisher'],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    publisherEntryLabel.place(x = 175, y = 200, width = 150, height = 50)

    publisheryearLabel = Label(confirmWithdrawal, text = "Publication Year",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    publisheryearLabel.place(x = 25, y = 250, width = 150, height = 50)
    publisheryearEntryLabel = Label(confirmWithdrawal, text = aa['yearPublished'],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    publisheryearEntryLabel.place(x = 175, y = 250, width = 150, height = 50)

    authorLabel = Label(confirmWithdrawal, text = "Author",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    authorLabel.place(x = 25, y = 300, width = 150, height = 50)
    authorEntryLabel = Label(confirmWithdrawal, text = aa['author_name'],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    authorEntryLabel.place(x = 175, y = 300, width = 150, height = 50)

    confirmButton = Button(confirmWithdrawal, text = "Confirm Withdrawal",
                       font = ("lucida", 15), wraplength = 100, command = lambda : withdraw_book(a))
    confirmButton.place(x = 50, y = 375, width = 100, height = 50)

    backButton = Button(confirmWithdrawal, text = "Back to Withdrawal Function",
                    font = ("lucida", 15), wraplength = 100, command = backTowithdraw)
    backButton.place(x = 200, y = 375, width = 100, height = 50)

def NErrorW(e):
    global noFineError
    noFineError = Toplevel()
    noFineError.title("Withdrawal Error")
    noFineError.geometry("300x300")
    noFineError.configure(bg = "red")

    def noFineErrorBackToWithdrawalFunction():
        noFineError.destroy()

    headerLabel = Label(noFineError, text = "Error!",
                    font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
    headerLabel.place(x = 75, y = 40, width = 150, height = 50)
    headerLabel.configure(foreground = "yellow")

    middleLabel = Label(noFineError, text = e,
                    font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
    middleLabel.place(x = 50, y = 150, width = 200, height = 50)
    middleLabel.configure(foreground = "yellow")

    backButton = Button(noFineError, text = "Back to Withdrawal Function",
                    font = ("lucida", 15), wraplength = 150, command = noFineErrorBackToWithdrawalFunction)
    backButton.place(x = 75, y = 240, width = 150, height = 40)





def loansMenuW():
    global loansMenu
    loansMenu = Toplevel()
    loansMenu.title("Books")
    loansMenu.geometry("1280x720")


    def loansMenuToBorrow():
        loansBorrowW()
        loansMenu.destroy()

    def loansMenuToReturn():
        loansReturnW()
        loansMenu.destroy()


    headerLabel = Label(loansMenu, text = "Select One of the Options Below:",
                        bg = "lightblue", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    borrowingButton = Button(loansMenu, text = "Book Borrowing", font = ("lucida", 18), command = loansMenuToBorrow)
    borrowingButton.place(x = 390, y = 150, width = 500, height = 60)

    returningButton = Button(loansMenu, text = "Book Returning", font = ("lucida", 18), command = loansMenuToReturn)
    returningButton.place(x = 390, y = 250, width = 500, height = 60)

    backButton = Button(loansMenu, text = "Back To Main Menu", command = lambda : [MenuW(), loansMenu.destroy()],
                        font = ("lucida", 16))
    backButton.place(x = 160, y = 600, width = 960, height = 50)

def loansBorrowW():
    global loansBorrow
    loansBorrow = Toplevel()
    loansBorrow.title("Books")
    loansBorrow.geometry("1280x720")


    headerLabel = Label(loansBorrow, text = "To Borrow a Book, Please Enter Information Below:",
                        font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    accessionNoLabel = Label(loansBorrow, text = "Accession Number: ", font = ("lucida", 18))
    accessionNoLabel.place(x = 300, y = 275, width = 170, height = 50)
    accessionNo = StringVar()
    accessionNoEntry = Entry(loansBorrow, textvariable = accessionNo)
    accessionNoEntry.place(x = 470, y = 275, width = 510, height = 50)

    memberIDLabel = Label(loansBorrow, text = "Membership ID: ", font = ("lucida", 18))
    memberIDLabel.place(x = 300, y = 350, width = 170, height = 50)
    memberID = StringVar()
    memberIDEntry = Entry(loansBorrow, textvariable = memberID)
    memberIDEntry.place(x = 470, y = 350, width = 510, height = 50)

    def loansBorrowToMenu():
        loansMenuW()
        loansBorrow.destroy()
    
    def loansBorrowLoanEW():
        global loansBorrowLoanE
        loansBorrowLoanE = Toplevel()
        loansBorrowLoanE.title("Borrow Error")
        loansBorrowLoanE.geometry("300x300")
        loansBorrowLoanE.configure(bg = "red")

        headerLabel = Label(loansBorrowLoanE, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(loansBorrowLoanE, text = "Book currently on Loan",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(loansBorrowLoanE, text = "Back to Borrow Function",
                            font = ("lucida", 15), wraplength = 150, command=loansBorrowLoanE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)

    def loansBorrowQuotaEW():
        global loansBorrowQuotaE
        loansBorrowQuotaE = Toplevel()
        loansBorrowQuotaE.title("Borrow Error")
        loansBorrowQuotaE.geometry("300x300")
        loansBorrowQuotaE.configure(bg = "red")

        headerLabel = Label(loansBorrowQuotaE, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(loansBorrowQuotaE, text = "Member loan quota exceeded.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(loansBorrowQuotaE, text = "Back to Borrow Function",
                            font = ("lucida", 15), wraplength = 150, command=loansBorrowQuotaE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)

    def loansBorrowFineEW():
        global loansBorrowFineE
        loansBorrowFineE = Toplevel()
        loansBorrowFineE.title("Borrow Error")
        loansBorrowFineE.geometry("300x300")
        loansBorrowFineE.configure(bg = "red")

        headerLabel = Label(loansBorrowFineE, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(loansBorrowFineE, text = "Member has outstanding fines.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(loansBorrowFineE, text = "Back to Borrow Function",
                            font = ("lucida", 15), wraplength = 150, command=loansBorrowFineE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)

    def loansReserveEW():
        global loansReserveEW
        loansReserveEW = Toplevel()
        loansReserveEW.title("Borrow Error")
        loansReserveEW.geometry("300x300")
        loansReserveEW.configure(bg = "red")

        headerLabel = Label(loansReserveEW, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(loansReserveEW, text = "Book is reserved.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(loansReserveEW, text = "Back to Borrow Function",
                            font = ("lucida", 15), wraplength = 150, command=loansReserveEW.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
    
    def loansOverdueEW():
        global loansOverdueEW
        loansOverdueEW = Toplevel()
        loansOverdueEW.title("Borrow Error")
        loansOverdueEW.geometry("300x300")
        loansOverdueEW.configure(bg = "red")

        headerLabel = Label(loansOverdueEW, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(loansOverdueEW, text = "Return overdue books",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(loansOverdueEW, text = "Back to Borrow Function",
                            font = ("lucida", 15), wraplength = 150, command=loansOverdueEW.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
    
    def loansBorrowConfirmW():
        global loansBorrowConfirm
        loansBorrowConfirm = Toplevel()
        loansBorrowConfirm.title("Confirm Loan")
        loansBorrowConfirm.geometry("350x500")
        loansBorrowConfirm.configure(bg = "SpringGreen3")

        try:
            bookNo = accessionNo.get()
            memberid = memberID.get()
        except:
            loansBorrowConfirm.destroy()
            messagebox.showerror(title = "Error!", message = "Invalid inputs or missing field!")

        if not member_exists(memberid):
            loansBorrowConfirm.destroy()
            messagebox.showerror(title = "Error!", message = "member does not exist!")
            raise ValueError("member does not exist!")
        elif not book_search(bookNo,'accessionNo'):
            loansBorrowConfirm.destroy()
            messagebox.showerror(title = "Error!", message = "book not registered")
            raise ValueError("book not registered")
        else:
            bookdetails = book_search(bookNo, 'accessionNo')
            borrow_date = datetime.now().date()
            due_Date = (datetime.now() + timedelta(14)).date()
            name = member_getName(memberid)

            accessionNoLabel = Label(loansBorrowConfirm,text = "Accession No",
                                    font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            accessionNoLabel.place(x = 25, y = 100, width = 150, height = 50)
                
            accession = Label(loansBorrowConfirm,text = bookdetails[0]['accessionNo'],
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            accession.place(x = 175, y = 100, width = 150, height = 50)
            
            titleLabel = Label(loansBorrowConfirm, text = "Book Title",
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            titleLabel.place(x = 25, y = 150, width = 150, height = 50)
            titleEntry= Label(loansBorrowConfirm, text = bookdetails[0]['title'],
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            titleEntry.place(x = 175, y = 150, width = 150, height = 50)

            borrowdateLabel = Label(loansBorrowConfirm, text = "Borrow Date",
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            borrowdateLabel.place(x = 25, y = 200, width = 150, height = 50)
            borrowdateEntryLabel = Label(loansBorrowConfirm, text = borrow_date,
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            borrowdateEntryLabel.place(x = 175, y = 200, width = 150, height = 50)

            memberIDLabel = Label(loansBorrowConfirm, text = "Membership ID",
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            memberIDLabel.place(x = 25, y = 250, width = 150, height = 50)
            memberIDEntryLabel = Label(loansBorrowConfirm, text = memberid,
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            memberIDEntryLabel.place(x = 175, y = 250, width = 150, height = 50)

            nameLabel = Label(loansBorrowConfirm, text = "Member Name",
                                font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            nameLabel.place(x = 25, y = 300, width = 150, height = 50)
            nameEntryLabel = Label(loansBorrowConfirm, text = name,
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            nameEntryLabel.place(x = 175, y = 300, width = 150, height = 50)

            duedateLabel = Label(loansBorrowConfirm, text = "Due Date",
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            duedateLabel.place(x = 25, y = 350, width = 150, height = 50)
            duedateEntryLabel = Label(loansBorrowConfirm, text = due_Date,
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
            duedateEntryLabel.place(x = 175, y = 350, width = 150, height = 50)
      
            headerLabel = Label(loansBorrowConfirm, text = "Confirm Loan Details To Be Correct",
                                font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
            headerLabel.place(x = 25, y = 0, width = 300, height = 100)

            confirmButton = Button(loansBorrowConfirm, text = "Confirm Loan", command=borrowbook,
                                font = ("lucida", 15), wraplength = 100)
            confirmButton.place(x = 50, y = 425, width = 100, height = 50)

            backButton = Button(loansBorrowConfirm, text = "Back to Borrow Function",
                                font = ("lucida", 15), wraplength = 100, command=loansBorrowConfirm.destroy)
            backButton.place(x = 200, y = 425, width = 100, height = 50)
        



    def loansConfirmToBorrow():
        loansBorrowW()
        loansBorrowConfirm.destroy()
    

    def borrowed():
        global borrowed
        borrowed = Toplevel()
        borrowed.title("book borrowed")
        borrowed.geometry("300x300")
        borrowed.configure(bg = "SpringGreen3")

        headerLabel = Label(borrowed, text = "Confirmed:",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "SpringGreen3")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)


        middleLabel = Label(borrowed, text = "You have borrowed the book!",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "SpringGreen3")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)


        backButton = Button(borrowed, text = "Back to Borrow Function",
                            font = ("lucida", 15), wraplength = 150, command=borrowed.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
    
    def borrowbook():
        
        try:
            bookNo = accessionNo.get()
            memberid = memberID.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")

        if not member_exists(memberid):
            return messagebox.showerror(title = "Error!", message = "member does not exist!")
        elif acquire_fine(memberid) > 0:
            loansBorrowFineEW()
            
        elif not notborrowed(bookNo):
            loansBorrowLoanEW()

        elif not memberCanBorrow(memberid):
            loansBorrowQuotaEW()

        elif overdue_book(memberid):
            loansOverdueEW()

        elif (not notreserved(bookNo)):
            if not memberReserved(memberid, bookNo) :
                loansReserveEW()
        else:            
            borrowed()
        borrow(bookNo, memberid)
        return

    borrowButton = Button(loansBorrow, text = "Borrow Book", font = ("lucida", 20), command = loansBorrowConfirmW)
    borrowButton.place(x = 375, y = 575, width = 225, height = 80)

    backToLoansButton = Button(loansBorrow, text = "Back To Loans Menu", font = ("lucida", 20), command = loansBorrowToMenu)
    backToLoansButton.place(x = 705, y = 575, width = 225, height = 80)

def loansReturnW():
    global loansReturn
    loansReturn = Toplevel()
    loansReturn.title("Books - Acquisition")
    loansReturn.geometry("1280x720")


    def loansReturnToMenu():
        loansMenuW()
        loansReturn.destroy()
    
    def validate_return_book():
        try:
            accession_number = accessionNo.get()
            return_date = date.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        if notborrowed(accession_number):
            return messagebox.showerror(title = "Error!", message = "Book not borrowed.")
        else:
            loansReturnConfirmW(accession_number)


    
    def loansReturnFineEW():
        global loansReturnFineE
        loansReturnFineE = Toplevel()
        loansReturnFineE.title("Return Error")
        loansReturnFineE.geometry("300x300")
        loansReturnFineE.configure(bg = "red")

        headerLabel = Label(loansReturnFineE, text = "Error!",
                            font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "yellow")

        middleLabel = Label(loansReturnFineE, text = "Book returned successfully but has fines.",
                            font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "yellow")

        backButton = Button(loansReturnFineE, text = "Back to Return Function",
                            font = ("lucida", 15), wraplength = 150, command=loansReturnFineE.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)
  
    def loansReturnConfirmW(accession_number):
        global loansReturnConfirm
        loansReturnConfirm = Toplevel()
        loansReturnConfirm.title("Confirm Return")
        loansReturnConfirm.geometry("350x450")
        loansReturnConfirm.configure(bg = "SpringGreen3")

        def return_book(accession_number):
            con = create_connection()
            cur = con.cursor()
            comment = "DELETE FROM BookLoan WHERE accessionNo = %s"
            memberID = borrow_getID(accession_number)[0]['memberID']
            dueDate = borrow_getDue(accession_number)[0]['dueDate']
            cur.execute(comment, accession_number)
            con.commit()
            con.close()
            if datetime.now().date() > dueDate:
                loansReturnFineEW()
            else:
                loansReturnSuccessW()
            return 

        headerLabel = Label(loansReturnConfirm, text = "Confirm Return Details To Be Correct",
                            font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
        headerLabel.place(x = 25, y = 0, width = 300, height = 100)

        bookdetails = book_search(accession_number, 'accessionNo')
        return_date = datetime.now().date()
        memberID = borrow_getID(accession_number)[0]['memberID']
        name = borrow_getName(accession_number)[0]['name']
        fine = update_fine(return_date, accession_number, memberID)
        accessionNoLabel = Label(loansReturnConfirm,text = "Accession No",
                                font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        accessionNoLabel.place(x = 25, y = 100, width = 150, height = 50)           
        accession = Label(loansReturnConfirm,text = bookdetails[0]['accessionNo'],
                        font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        accession.place(x = 175, y = 100, width = 150, height = 50)

        titleLabel = Label(loansReturnConfirm, text = "Book Title",
                        font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        titleLabel.place(x = 25, y = 150, width = 150, height = 50)
        titleEntry= Label(loansReturnConfirm, text = bookdetails[0]['title'],
                        font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        titleEntry.place(x = 175, y = 150, width = 150, height = 50)

        memberIDLabel = Label(loansReturnConfirm, text = "Membership ID",
                        font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        memberIDLabel.place(x = 25, y = 200, width = 150, height = 50)
        memberIDEntryLabel = Label(loansReturnConfirm, text = memberID,
                        font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        memberIDEntryLabel.place(x = 175, y = 200, width = 150, height = 50)

        nameLabel = Label(loansReturnConfirm, text = "Member Name",
                            font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        nameLabel.place(x = 25, y = 250, width = 150, height = 50)
        nameEntryLabel = Label(loansReturnConfirm, text = name,
                        font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        nameEntryLabel.place(x = 175, y = 250, width = 150, height = 50)

        returndateLabel = Label(loansReturnConfirm, text = "Return Date",
                        font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        returndateLabel.place(x = 25, y = 300, width = 150, height = 50)
        returndateEntryLabel = Label(loansReturnConfirm, text = return_date,
                        font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        returndateEntryLabel.place(x = 175, y = 300, width = 150, height = 50)

        fineLabel = Label(loansReturnConfirm, text = "Fine", 
                            font = ("lcuida", 15), wraplength = 150, bg = "SpringGreen3")
        fineLabel.place(x = 25, y = 350, width = 150, height = 50)
        fineEntryLabel = Label(loansReturnConfirm, text = fine,
                                font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
        fineEntryLabel.place(x = 175, y = 350, width = 150, height = 50)

        confirmButton = Button(loansReturnConfirm, text = "Confirm Return",
                            font = ("lucida", 15), wraplength = 100, command = lambda : return_book(accession_number))
        confirmButton.place(x = 50, y = 400, width = 100, height = 50)

        backButton = Button(loansReturnConfirm, text = "Back to Return Function",
                            font = ("lucida", 15), wraplength = 100, command=loansReturnConfirm.destroy)
        backButton.place(x = 200, y = 400, width = 100, height = 50)
    
    def loansReturnSuccessW():
        global loansReturnSuccessW
        loansReturnSuccessW = Toplevel()
        loansReturnSuccessW.title("Book Return Success")
        loansReturnSuccessW.geometry("300x300")
        loansReturnSuccessW.configure(bg = "SpringGreen3")

        headerLabel = Label(loansReturnSuccessW, text = "Sucess!", font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "SpringGreen3")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "black")

        middleLabel = Label(loansReturnSuccessW, text = "Book Returned.", font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "SpringGreen3")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "black")

        backButton = Button(loansReturnSuccessW, text = "Back to Return Function", font = ("lucida", 15), wraplength = 150, command=loansReturnSuccessW.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)


    headerLabel = Label(loansReturn, text = "To Return a Book, Please Enter Information Below:",
                        font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    accessionNoLabel = Label(loansReturn, text = "Accession Number: ", font = ("lucida", 18))
    accessionNoLabel.place(x = 300, y = 275, width = 170, height = 50)
    accessionNo = StringVar()
    accessionNoEntry = Entry(loansReturn, textvariable = accessionNo)
    accessionNoEntry.place(x = 470, y = 275, width = 510, height = 50)

    dateLabel = Label(loansReturn, text = "Return Date: ", font = ("lucida", 18))
    dateLabel.place(x = 300, y = 350, width = 170, height = 50)
    date = StringVar()
    dateEntry = Entry(loansReturn, textvariable = date)
    dateEntry.place(x = 470, y = 350, width = 510, height = 50)

    returnButton = Button(loansReturn, text = "Return Book", font = ("lucida", 20), command = validate_return_book)
    returnButton.place(x = 375, y = 575, width = 225, height = 80)

    backToLoansButton = Button(loansReturn, text = "Back To Loans Menu", font = ("lucida", 20), command = loansReturnToMenu)
    backToLoansButton.place(x = 705, y = 575, width = 225, height = 80)









'''




def reservationMenuW():
    global reservationMenu
    reservationMenu = Toplevel()
    reservationMenu.title("Reservations")
    reservationMenu.geometry("1280x720")

    def reservationMenuToReserve():
        bookReservationW()
        reservationMenu.destroy()

    def reservationMenuToCancel():
        cancelReservationW()
        reservationMenu.destroy()

    headerLabel = Label(reservationMenu, text = "Select One of the Options Below:",
                    bg = "lightblue", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    reserveButton = Button(reservationMenu, text = "Reserve a Book",
                       font = ("lucida", 18 ), command = reservationMenuToReserve)
    reserveButton.place(x = 390, y = 150, width = 500, height = 60)

    cancelButton = Button(reservationMenu, text = "Cancel Reservation",
                       font = ("lucida", 18 ), command = reservationMenuToCancel)
    cancelButton.place(x = 390, y = 250, width = 500, height = 60)

    backButton = Button(reservationMenu, text = "Back To Main Menu", command = lambda : [MenuW(), reservationMenu.destroy()],
                    font = ("lucida", 16))
    backButton.place(x = 160, y = 600, width = 960, height = 50)


def bookReservationW():
    global bookReservation
    bookReservation = Toplevel()
    bookReservation.title("Reservation - Make a Reservation")
    bookReservation.geometry("1280x720")

   

    def reserveToMenu():
        reservationMenuW()
        bookReservation.destroy()
        
    def reserveBook():
        an = accessionNo.get()
        me = membershipID.get()
        d= datetime.now().date()
        k = info2(an,me)
        if info2(an,me)[0]:
            k[1].append(d)
            confirmReservationW(k[1])
        else:
            top= Toplevel(root)
            top.geometry("640x360")
            top.title("")
            Label(top, text= info2(an,me)[1]).place(x=150,y=80)
            top.after(2000,top.destroy)
            bookReservation.destroy()
            bookReservationW()
    


    headerLabel = Label(bookReservation, text = "To Reserve a Book, Please Enter Information Below:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    accessionNoLabel = Label(bookReservation, text = "Accession Number: ", font = ("lucida", 18))
    accessionNoLabel.place(x = 300, y = 125, width = 170, height = 50)
    accessionNo = StringVar()
    accessionNoEntry = Entry(bookReservation, textvariable = accessionNo)
    accessionNoEntry.place(x = 470, y = 125, width = 510, height = 50)

    membershipIDLabel = Label(bookReservation, text = "Membership ID: ", font = ("lucida", 18))
    membershipIDLabel.place(x = 300, y = 200, width = 170, height = 50)
    membershipID = StringVar()
    membershipIDEntry = Entry(bookReservation, textvariable = membershipID)
    membershipIDEntry.place(x = 470, y = 200, width = 510, height = 50)

    reserveDateLabel = Label(bookReservation, text = "Reserve date: ", font = ("lucida", 18))
    reserveDateLabel.place(x = 300, y = 275, width = 170, height = 50)
    reserveDate = StringVar()
    reserveDateEntry = Entry(bookReservation, textvariable = reserveDate)
    reserveDateEntry.place(x = 470, y = 275, width = 510, height = 50)
    reserveDateEntry.delete(0, END)

    reserveButton = Button(bookReservation, text = "Reserve Book",
                           font = ("lucida", 20), command = reserveBook )
    reserveButton.place(x = 375, y = 575, width = 225, height = 80)

    backButton = Button(bookReservation, text = "Back To Reservations Menu",
                        font = ("lucida", 20), wraplength = 150, command = reserveToMenu)
    backButton.place(x = 705, y = 575, width = 225, height = 80)



def cancelReservationW():
    global cancelReservation
    cancelReservation = Toplevel()
    cancelReservation.title("Reservation - Cancel Reservation")
    cancelReservation.geometry("1280x720")

    def cancelbook():
        an = accessionNo.get()
        me = membershipID.get()
        d= datetime.now().date()
        k = info2(an,me)
        if k[0]:
            k[1].append(d)
            confirmCancellationW(k[1])
        else:
            top= Toplevel(root)
            top.geometry("640x360")
            top.title("")
            top.configure(bg = "red")
            Label(top, text= k[1], font = ('lucida',25)).place(x=150,y=80)
            top.after(2000,top.destroy)
            cancelReservation.destroy()
            cancelReservationW()


    def cancelToMenu():
        reservationMenuW()
        cancelReservation.destroy()

    headerLabel = Label(cancelReservation, text = "To Cancel a Reservation, Please Enter Information Below:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    accessionNoLabel = Label(cancelReservation, text = "Accession Number: ", font = ("lucida", 18))
    accessionNoLabel.place(x = 300, y = 125, width = 170, height = 50)
    accessionNo = StringVar()
    accessionNoEntry = Entry(cancelReservation, textvariable = accessionNo)
    accessionNoEntry.place(x = 470, y = 125, width = 510, height = 50)

    membershipIDLabel = Label(cancelReservation, text = "Membership ID: ", font = ("lucida", 18))
    membershipIDLabel.place(x = 300, y = 200, width = 170, height = 50)
    membershipID = StringVar()
    membershipIDEntry = Entry(cancelReservation, textvariable = membershipID)
    membershipIDEntry.place(x = 470, y = 200, width = 510, height = 50)

    cancelDateLabel = Label(cancelReservation, text = "Cancel date: ", font = ("lucida", 18))
    cancelDateLabel.place(x = 300, y = 275, width = 170, height = 50)
    cancelDate = StringVar()
    cancelDateEntry = Entry(cancelReservation, textvariable = cancelDate)
    cancelDateEntry.place(x = 470, y = 275, width = 510, height = 50)
    cancelDateEntry.delete(0, END)

    cancelButton = Button(cancelReservation, text = "Cancel Reservation", command = cancelbook,font = ("lucida", 20))
    cancelButton.place(x = 375, y = 575, width = 225, height = 80)

    backButton = Button(cancelReservation, text = "Back To Reservations Menu",
                        font = ("lucida", 20), wraplength = 150, command = cancelToMenu)
    backButton.place(x = 705, y = 575, width = 225, height = 80)

def reservationErrorW(ll):
    global reservationError
    reservationError = Toplevel()
    reservationError.title("Reservation Error")
    reservationError.geometry("300x300")
    reservationError.configure(bg = "red")

    def reservationErrorBackToMenu():
        
        reservationError.destroy()

    headerLabel = Label(reservationError, text = "Error!",
                    font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
    headerLabel.place(x = 75, y = 40, width = 150, height = 50)
    headerLabel.configure(foreground = "yellow")

    middleLabel = Label(reservationError, text = ll,
                    font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
    middleLabel.place(x = 50, y = 150, width = 200, height = 50)
    middleLabel.configure(foreground = "yellow")

    backButton = Button(reservationError, text = "Back to Reserve Function",
                    font = ("lucida", 15), wraplength = 150, command = reservationErrorBackToMenu)
    backButton.place(x = 75, y = 240, width = 150, height = 40)




def confirmReservationW(l):
    global confirmReservation
    confirmReservation = Toplevel()
    confirmReservation.title("Confirm Reservation")
    confirmReservation.geometry("350x450")
    confirmReservation.configure(bg = "SpringGreen3")

    def confirmreservation():
        if reserve(l[2],l[0],l[-1])[0]:
            top= Toplevel(root)
            top.geometry("1280x720")
            top.configure(bg = "SpringGreen3")
            top.title("")
            Label(top, text = f'Success',
            font = ("lucida", 50)).place(x=520,y=30)
            top.after(2000,top.destroy)
        else:
            reservationErrorW(reserve(l[2],l[0],l[-1])[1])

    def backToReserveFunction():
        confirmReservation.destroy()

    headerLabel = Label(confirmReservation, text = "Confirm Reservation Details To Be Correct",
                    font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
    headerLabel.place(x = 25, y = 0, width = 300, height = 100)

    accessionNumberLabel = Label(confirmReservation,text = f"Accession Number",
                             font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    accessionNumberLabel.place(x = 25, y = 100, width = 150, height = 50)
    accessionNumberEntryLabel = Label(confirmReservation,text = l[2],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    accessionNumberEntryLabel.place(x = 175, y = 100, width = 150, height = 50)

    bookTitleLabel = Label(confirmReservation, text = "Book Title",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    bookTitleLabel.place(x = 25, y = 150, width = 150, height = 50)
    bookTitleEntryLabel = Label(confirmReservation, text = l[3],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    bookTitleEntryLabel.place(x = 175, y = 150, width = 150, height = 50)

    membershipIDLabel = Label(confirmReservation, text = "Membership ID",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDLabel.place(x = 25, y = 200, width = 150, height = 50)
    membershipIDEntryLabel = Label(confirmReservation, text = l[0],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDEntryLabel.place(x = 175, y = 200, width = 150, height = 50)

    memberNameLabel = Label(confirmReservation, text = "Member Name",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    memberNameLabel.place(x = 25, y = 250, width = 150, height = 50)
    memberNameEntryLabel = Label(confirmReservation, text = l[1],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    memberNameEntryLabel.place(x = 175, y = 250, width = 150, height = 50)

    reserveDateLabel = Label(confirmReservation, text = "Reserve Date",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    reserveDateLabel.place(x = 25, y = 300, width = 150, height = 50)
    reserveDateEntryLabel = Label(confirmReservation, text = l[-1],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    reserveDateEntryLabel.place(x = 175, y = 300, width = 150, height = 50)

    confirmButton = Button(confirmReservation, text = "Confirm Reservation",
                       font = ("lucida", 15), wraplength = 100, command = lambda : [confirmreservation(),confirmReservation.destroy()])
    confirmButton.place(x = 50, y = 375, width = 100, height = 50)

    backButton = Button(confirmReservation, text = "Back to Reserve Function",
                    font = ("lucida", 15), wraplength = 100, command = backToReserveFunction)
    backButton.place(x = 200, y = 375, width = 100, height = 50)

def confirmCancellationW(l):
    global confirmCancellation
    confirmCancellation = Toplevel()
    confirmCancellation.title("Confirm Reservation")
    confirmCancellation.geometry("350x450")
    confirmCancellation.configure(bg = "SpringGreen3")

    def cCancellation():
       
        if deletereserve(l[2],l[0],l[-1]):
            top= Toplevel(root)
            top.geometry("1280x720")
            top.title("")
            Label(top, text = f'Success',
            font = ("lucida", 50)).place(x=520,y=30)
            top.after(2000,top.destroy)
        else:
            cancellationErrorW()
        
        

    def backToCancellationMenu():
        confirmCancellation.destroy()

    headerLabel = Label(confirmCancellation, text = "Confirm Reservation Details To Be Correct",
                    font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
    headerLabel.place(x = 25, y = 0, width = 300, height = 100)

    accessionNumberLabel = Label(confirmCancellation,text = "Accession Number",
                             font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    accessionNumberLabel.place(x = 25, y = 100, width = 150, height = 50)
    accessionNumberEntryLabel = Label(confirmCancellation, text = l[2] , 
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    accessionNumberEntryLabel.place(x = 175, y = 100, width = 150, height = 50)

    bookTitleLabel = Label(confirmCancellation, text = "Book Title",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    bookTitleLabel.place(x = 25, y = 150, width = 150, height = 50)
    bookTitleEntryLabel = Label(confirmCancellation, text = l[3] ,
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    bookTitleEntryLabel.place(x = 175, y = 150, width = 150, height = 50)

    membershipIDLabel = Label(confirmCancellation, text = "Membership ID",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDLabel.place(x = 25, y = 200, width = 150, height = 50)
    membershipIDEntryLabel = Label(confirmCancellation, text = l[0],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDEntryLabel.place(x = 175, y = 200, width = 150, height = 50)

    memberNameLabel = Label(confirmCancellation, text = "Member Name",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    memberNameLabel.place(x = 25, y = 250, width = 150, height = 50)
    memberNameEntryLabel = Label(confirmCancellation, text = l[1],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    memberNameEntryLabel.place(x = 175, y = 250, width = 150, height = 50)

    reserveDateLabel = Label(confirmCancellation, text = "Reserve Date",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    reserveDateLabel.place(x = 25, y = 300, width = 150, height = 50)
    reserveDateEntryLabel = Label(confirmCancellation, text = l[-1],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    reserveDateEntryLabel.place(x = 175, y = 300, width = 150, height = 50)

    confirmButton = Button(confirmCancellation, text = "Confirm Cancellation",
                       font = ("lucida", 15), wraplength = 100, command = lambda : [cCancellation(),confirmCancellation.destroy()])
    confirmButton.place(x = 50, y = 375, width = 100, height = 50)

    backButton = Button(confirmCancellation, text = "Back to Cancellation Function",
                    font = ("lucida", 15), wraplength = 100, command = backToCancellationMenu)
    backButton.place(x = 200, y = 375, width = 100, height = 50)

def cancellationErrorW():
    global cancellationError
    cancellationError = Toplevel()
    cancellationError.title("Cancellation Error")
    cancellationError.geometry("300x300")
    cancellationError.configure(bg = "red")

    def errorBackToCancellationFunction():
        cancellationError.destroy()

    headerLabel = Label(cancellationError, text = "Error!",
                    font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
    headerLabel.place(x = 75, y = 40, width = 150, height = 50)
    headerLabel.configure(foreground = "yellow")

    middleLabel = Label(cancellationError, text = "Member has no such reservation. OR Book is currently not on loan.",
                    font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
    middleLabel.place(x = 50, y = 150, width = 200, height = 50)
    middleLabel.configure(foreground = "yellow")

    backButton = Button(cancellationError, text = "Back to Cancellation Function",
                    font = ("lucida", 15), wraplength = 150, command = errorBackToCancellationFunction)
    backButton.place(x = 75, y = 240, width = 150, height = 40)

'''

def reservationMenuW():
    global reservationMenu
    reservationMenu = Toplevel()
    reservationMenu.title("Reservations")
    reservationMenu.geometry("1280x720")

    def reservationMenuToReserve():
        bookReservationW()
        reservationMenu.destroy()

    def reservationMenuToCancel():
        cancelReservationW()
        reservationMenu.destroy()

    headerLabel = Label(reservationMenu, text = "Select One of the Options Below:",
                    bg = "lightblue", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    reserveButton = Button(reservationMenu, text = "Reserve a Book",
                       font = ("lucida", 18 ), command = reservationMenuToReserve)
    reserveButton.place(x = 390, y = 150, width = 500, height = 60)

    cancelButton = Button(reservationMenu, text = "Cancel Reservation",
                       font = ("lucida", 18 ), command = reservationMenuToCancel)
    cancelButton.place(x = 390, y = 250, width = 500, height = 60)

    backButton = Button(reservationMenu, text = "Back To Main Menu", command = lambda : [MenuW(), reservationMenu.destroy()],
                    font = ("lucida", 16))
    backButton.place(x = 160, y = 600, width = 960, height = 50)


def bookReservationW():
    global bookReservation
    bookReservation = Toplevel()
    bookReservation.title("Reservation - Make a Reservation")
    bookReservation.geometry("1280x720")

   

    def reserveToMenu():
        reservationMenuW()
        bookReservation.destroy()
        
    def reserveBook():
        an = accessionNo.get()
        me = membershipID.get()
        d= reserveDate.get()
        k = info2(an,me)
        if info2(an,me)[0]:
            k[1].append(d)
            confirmReservationW(k[1])
        else:
            top= Toplevel(root)
            top.geometry("640x360")
            top.title("")
            Label(top, text= info2(an,me)[1]).place(x=150,y=80)
            top.after(2000,top.destroy)
            bookReservation.destroy()
            bookReservationW()
    


    headerLabel = Label(bookReservation, text = "To Reserve a Book, Please Enter Information Below:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    accessionNoLabel = Label(bookReservation, text = "Accession Number: ", font = ("lucida", 18))
    accessionNoLabel.place(x = 300, y = 125, width = 170, height = 50)
    accessionNo = StringVar()
    accessionNoEntry = Entry(bookReservation, textvariable = accessionNo)
    accessionNoEntry.place(x = 470, y = 125, width = 510, height = 50)

    membershipIDLabel = Label(bookReservation, text = "Membership ID: ", font = ("lucida", 18))
    membershipIDLabel.place(x = 300, y = 200, width = 170, height = 50)
    membershipID = StringVar()
    membershipIDEntry = Entry(bookReservation, textvariable = membershipID)
    membershipIDEntry.place(x = 470, y = 200, width = 510, height = 50)

    reserveDateLabel = Label(bookReservation, text = "Reserve date: ", font = ("lucida", 18))
    reserveDateLabel.place(x = 300, y = 275, width = 170, height = 50)
    reserveDate = StringVar()
    reserveDateEntry = Entry(bookReservation, textvariable = reserveDate)
    reserveDateEntry.place(x = 470, y = 275, width = 510, height = 50)
    reserveDateEntry.delete(0, END)

    reserveButton = Button(bookReservation, text = "Reserve Book",
                           font = ("lucida", 20), command = reserveBook )
    reserveButton.place(x = 375, y = 575, width = 225, height = 80)

    backButton = Button(bookReservation, text = "Back To Reservations Menu",
                        font = ("lucida", 20), wraplength = 150, command = reserveToMenu)
    backButton.place(x = 705, y = 575, width = 225, height = 80)


def cancelReservationW():
    global cancelReservation
    cancelReservation = Toplevel()
    cancelReservation.title("Reservation - Cancel Reservation")
    cancelReservation.geometry("1280x720")

    def cancelbook():
        try:
            an = accessionNo.get()
            me = membershipID.get()
            d= cancelDate.get()
        except:
            cancellationErrorW("Missing or incomplete fields.")
            return
        else:
            if not is_member(me):
                cancellationErrorW("Member does not exist.")
            elif not book_exist(an):
                cancellationErrorW("Book does not exist.")
            elif not memberReserved(me, an):
                cancellationErrorW("Member has no such reservation.")
            else:
                confirmCancellationW(an, me, d)



    def cancelToMenu():
        reservationMenuW()
        cancelReservation.destroy()

    headerLabel = Label(cancelReservation, text = "To Cancel a Reservation, Please Enter Information Below:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    accessionNoLabel = Label(cancelReservation, text = "Accession Number: ", font = ("lucida", 18))
    accessionNoLabel.place(x = 300, y = 125, width = 170, height = 50)
    accessionNo = StringVar()
    accessionNoEntry = Entry(cancelReservation, textvariable = accessionNo)
    accessionNoEntry.place(x = 470, y = 125, width = 510, height = 50)

    membershipIDLabel = Label(cancelReservation, text = "Membership ID: ", font = ("lucida", 18))
    membershipIDLabel.place(x = 300, y = 200, width = 170, height = 50)
    membershipID = StringVar()
    membershipIDEntry = Entry(cancelReservation, textvariable = membershipID)
    membershipIDEntry.place(x = 470, y = 200, width = 510, height = 50)

    cancelDateLabel = Label(cancelReservation, text = "Cancel date: ", font = ("lucida", 18))
    cancelDateLabel.place(x = 300, y = 275, width = 170, height = 50)
    cancelDate = StringVar()
    cancelDateEntry = Entry(cancelReservation, textvariable = cancelDate)
    cancelDateEntry.place(x = 470, y = 275, width = 510, height = 50)
    cancelDateEntry.delete(0, END)

    cancelButton = Button(cancelReservation, text = "Cancel Reservation", command = cancelbook,font = ("lucida", 20))
    cancelButton.place(x = 375, y = 575, width = 225, height = 80)

    backButton = Button(cancelReservation, text = "Back To Reservations Menu",
                        font = ("lucida", 20), wraplength = 150, command = cancelToMenu)
    backButton.place(x = 705, y = 575, width = 225, height = 80)

def reservationErrorW(ll):
    global reservationError
    reservationError = Toplevel()
    reservationError.title("Reservation Error")
    reservationError.geometry("300x300")
    reservationError.configure(bg = "red")

    def reservationErrorBackToMenu():
        
        reservationError.destroy()

    headerLabel = Label(reservationError, text = "Error!",
                    font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
    headerLabel.place(x = 75, y = 40, width = 150, height = 50)
    headerLabel.configure(foreground = "yellow")

    middleLabel = Label(reservationError, text = ll,
                    font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
    middleLabel.place(x = 50, y = 150, width = 200, height = 50)
    middleLabel.configure(foreground = "yellow")

    backButton = Button(reservationError, text = "Back to Reserve Function",
                    font = ("lucida", 15), wraplength = 150, command = reservationErrorBackToMenu)
    backButton.place(x = 75, y = 240, width = 150, height = 40)




def confirmReservationW(l):
    global confirmReservation
    confirmReservation = Toplevel()
    confirmReservation.title("Confirm Reservation")
    confirmReservation.geometry("350x450")
    confirmReservation.configure(bg = "SpringGreen3")

    def confirmreservation():
        accessionid = l[2]
        memberid = l[0]
        reservedate = l[-1]
        y=""
        if not member_exists(memberid):
            y = "member does not exist"
            reservationErrorW(y)
            return
        elif not book_exist(accessionid):
            y = "book not registered"
            reservationErrorW(y)
            return
        elif memberReserved(memberid, accessionid):
            y="You have already reserve the book"
            reservationErrorW(y)
            return
        elif isreserve(accessionid, memberid) != 'yes':
            y = 'Book is reserve'
            reservationErrorW(y)
            return
        elif not isborrow(accessionid):
            y = 'Book is not on loan'
            reservationErrorW(y)
            return
        elif not (reservecount(memberid)):
            y = "Reservation limit reached"
            reservationErrorW(y)
            return
        elif hasfine(memberid):
            y = "Please pay fine"
            reservationErrorW(y)
            return
        else:
            reserve(accessionid, memberid, reservedate)
            top= Toplevel(root)
            top.geometry("1280x720")
            top.title("")
            Label(top, text = f'Success',
            font = ("lucida", 50)).place(x=520,y=30)
            top.after(2000,top.destroy)
            return

    def backToReserveFunction():
        confirmReservation.destroy()

    headerLabel = Label(confirmReservation, text = "Confirm Reservation Details To Be Correct",
                    font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
    headerLabel.place(x = 25, y = 0, width = 300, height = 100)

    accessionNumberLabel = Label(confirmReservation,text = f"Accession Number",
                             font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    accessionNumberLabel.place(x = 25, y = 100, width = 150, height = 50)
    accessionNumberEntryLabel = Label(confirmReservation,text = l[2],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    accessionNumberEntryLabel.place(x = 175, y = 100, width = 150, height = 50)

    bookTitleLabel = Label(confirmReservation, text = "Book Title",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    bookTitleLabel.place(x = 25, y = 150, width = 150, height = 50)
    bookTitleEntryLabel = Label(confirmReservation, text = l[3],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    bookTitleEntryLabel.place(x = 175, y = 150, width = 150, height = 50)

    membershipIDLabel = Label(confirmReservation, text = "Membership ID",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDLabel.place(x = 25, y = 200, width = 150, height = 50)
    membershipIDEntryLabel = Label(confirmReservation, text = l[0],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDEntryLabel.place(x = 175, y = 200, width = 150, height = 50)

    memberNameLabel = Label(confirmReservation, text = "Member Name",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    memberNameLabel.place(x = 25, y = 250, width = 150, height = 50)
    memberNameEntryLabel = Label(confirmReservation, text = l[1],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    memberNameEntryLabel.place(x = 175, y = 250, width = 150, height = 50)

    reserveDateLabel = Label(confirmReservation, text = "Reserve Date",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    reserveDateLabel.place(x = 25, y = 300, width = 150, height = 50)
    reserveDateEntryLabel = Label(confirmReservation, text = l[-1],
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    reserveDateEntryLabel.place(x = 175, y = 300, width = 150, height = 50)

    confirmButton = Button(confirmReservation, text = "Confirm Reservation",
                       font = ("lucida", 15), wraplength = 100, command = lambda : [confirmreservation(),confirmReservation.destroy()])
    confirmButton.place(x = 50, y = 375, width = 100, height = 50)

    backButton = Button(confirmReservation, text = "Back to Reserve Function",
                    font = ("lucida", 15), wraplength = 100, command = backToReserveFunction)
    backButton.place(x = 200, y = 375, width = 100, height = 50)

def confirmCancellationW(accesion_number, member_id, cancel_date):
    global confirmCancellation
    confirmCancellation = Toplevel()
    confirmCancellation.title("Confirm Reservation")
    confirmCancellation.geometry("350x450")
    confirmCancellation.configure(bg = "SpringGreen3")

    """
    def cCancellation():
       
        if deletereserve(l[2],l[0],l[-1]):
            top= Toplevel(root)
            top.geometry("1280x720")
            top.title("")
            Label(top, text = f'Success',
            font = ("lucida", 50)).place(x=520,y=30)
            top.after(2000,top.destroy)
        else:
            cancellationErrorW()
    """

    def confirm_delete(accesion_number, member_id, cancel_date):
        deletereserve(accesion_number, member_id, cancel_date)
        deleteReserveSuccessW()

    def backToCancellationMenu():
        confirmCancellation.destroy()
    
    def deleteReserveSuccessW():
        global deleteReserveSuccess
        deleteReserveSuccess = Toplevel()
        deleteReserveSuccess.title("Reserve Deletion Successful")
        deleteReserveSuccess.geometry("300x300")
        deleteReserveSuccess.configure(bg = "SpringGreen3")

        headerLabel = Label(deleteReserveSuccess, text = "Sucess!", font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "SpringGreen3")
        headerLabel.place(x = 75, y = 40, width = 150, height = 50)
        headerLabel.configure(foreground = "black")

        middleLabel = Label(deleteReserveSuccess, text = "Reservation Successfully Deleted", font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "SpringGreen3")
        middleLabel.place(x = 50, y = 150, width = 200, height = 50)
        middleLabel.configure(foreground = "black")

        backButton = Button(deleteReserveSuccess, text = "Back to Delete Function", font = ("lucida", 15), wraplength = 150, command=deleteReserveSuccess.destroy)
        backButton.place(x = 75, y = 240, width = 150, height = 40)

    headerLabel = Label(confirmCancellation, text = "Confirm Reservation Details To Be Correct",
                    font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
    headerLabel.place(x = 25, y = 0, width = 300, height = 100)

    accessionNumberLabel = Label(confirmCancellation,text = "Accession Number",
                             font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    accessionNumberLabel.place(x = 25, y = 100, width = 150, height = 50)
    accessionNumberEntryLabel = Label(confirmCancellation, text = accesion_number , 
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    accessionNumberEntryLabel.place(x = 175, y = 100, width = 150, height = 50)

    bookTitleLabel = Label(confirmCancellation, text = "Book Title",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    bookTitleLabel.place(x = 25, y = 150, width = 150, height = 50)
    bookTitleEntryLabel = Label(confirmCancellation, text =  book_getTitle(accesion_number),
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    bookTitleEntryLabel.place(x = 175, y = 150, width = 150, height = 50)

    membershipIDLabel = Label(confirmCancellation, text = "Membership ID",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDLabel.place(x = 25, y = 200, width = 150, height = 50)
    membershipIDEntryLabel = Label(confirmCancellation, text = member_id,
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDEntryLabel.place(x = 175, y = 200, width = 150, height = 50)

    memberNameLabel = Label(confirmCancellation, text = "Member Name",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    memberNameLabel.place(x = 25, y = 250, width = 150, height = 50)
    memberNameEntryLabel = Label(confirmCancellation, text = member_getName(member_id),
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    memberNameEntryLabel.place(x = 175, y = 250, width = 150, height = 50)

    reserveDateLabel = Label(confirmCancellation, text = "Reserve Date",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    reserveDateLabel.place(x = 25, y = 300, width = 150, height = 50)
    reserveDateEntryLabel = Label(confirmCancellation, text = cancel_date,
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    reserveDateEntryLabel.place(x = 175, y = 300, width = 150, height = 50)

    confirmButton = Button(confirmCancellation, text = "Confirm Cancellation",
                       font = ("lucida", 15), wraplength = 100, command = lambda : confirm_delete(accesion_number, member_id, cancel_date))
    confirmButton.place(x = 50, y = 375, width = 100, height = 50)

    backButton = Button(confirmCancellation, text = "Back to Cancellation Function",
                    font = ("lucida", 15), wraplength = 100, command = backToCancellationMenu)
    backButton.place(x = 200, y = 375, width = 100, height = 50)

def cancellationErrorW(error_message):
    global cancellationError
    cancellationError = Toplevel()
    cancellationError.title("Cancellation Error")
    cancellationError.geometry("300x300")
    cancellationError.configure(bg = "red")

    def errorBackToCancellationFunction():
        cancellationError.destroy()

    headerLabel = Label(cancellationError, text = "Error!",
                    font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
    headerLabel.place(x = 75, y = 40, width = 150, height = 50)
    headerLabel.configure(foreground = "yellow")

    middleLabel = Label(cancellationError, text = error_message,
                    font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
    middleLabel.place(x = 50, y = 150, width = 200, height = 50)
    middleLabel.configure(foreground = "yellow")

    backButton = Button(cancellationError, text = "Back to Cancellation Function",
                    font = ("lucida", 15), wraplength = 150, command = errorBackToCancellationFunction)
    backButton.place(x = 75, y = 240, width = 150, height = 40)



def finesMenuW():
    global finesMenu
    finesMenu = Toplevel()
    finesMenu.title("Fines")
    finesMenu.geometry("1280x720")

    def finesMenuToPayment():
        paymentW()
        finesMenu.destroy()

    headerLabel = Label(finesMenu, text = "Select One of the Options Below:",
                    bg = "lightblue", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    paymentButton = Button(finesMenu, text = "Payment",
                       font = ("lucida", 18 ), command = finesMenuToPayment)

    paymentButton.place(x = 390, y = 150, width = 500, height = 60)

    backButton = Button(finesMenu, text = "Back To Main Menu", command = lambda : [MenuW(), finesMenu.destroy()],
                    font = ("lucida", 16))
    backButton.place(x = 160, y = 600, width = 960, height = 50)

def paymentW():
    global finePayment
    finePayment = Toplevel()
    finePayment.title("Fines - Fine Payment")
    finePayment.geometry("1280x720")

    def paymentToMenu():
        finesMenuW()
        finePayment.destroy()

    def payment():
        me = membershipID.get()
        d = paymentDate.get()
        a = paymentAmount.get()
        confirmPaymentW(me,d,a)

    headerLabel = Label(finePayment, text = "To Pay a Fine, Please Enter Information Below:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    membershipIDLabel = Label(finePayment, text = "Membership ID: ", font = ("lucida", 18))
    membershipIDLabel.place(x = 300, y = 125, width = 170, height = 50)
    membershipID = StringVar()
    membershipIDEntry = Entry(finePayment, textvariable = membershipID)
    membershipIDEntry.place(x = 470, y = 125, width = 510, height = 50)

    paymentDateLabel = Label(finePayment, text = "Payment Date: ", font = ("lucida", 18))
    paymentDateLabel.place(x = 300, y = 200, width = 170, height = 50)
    paymentDate = StringVar()
    paymentDateEntry = Entry(finePayment, textvariable = paymentDate)
    paymentDateEntry.place(x = 470, y = 200, width = 510, height = 50)

    paymentAmountLabel = Label(finePayment, text = "Payment Amount: ", font = ("lucida", 18))
    paymentAmountLabel.place(x = 300, y = 275, width = 170, height = 50)
    paymentAmount = IntVar()
    paymentAmountEntry = Entry(finePayment, textvariable = paymentAmount)
    paymentAmountEntry.place(x = 470, y = 275, width = 510, height = 50)

    payButton = Button(finePayment, text = "Pay Fine",
                       font = ("lucida", 20), command = payment)
    payButton.place(x = 375, y = 575, width = 225, height = 80)

    backButton = Button(finePayment, text = "Back To Fines Menu",
                        font = ("lucida", 20), wraplength = 150, command = paymentToMenu)
    backButton.place(x = 705, y = 575, width = 225, height = 80)

def confirmPaymentW(me,d,a):
    global confirmPayment
    confirmPayment = Toplevel()
    confirmPayment.title("Confirm Payment")
    confirmPayment.geometry("350x450")
    confirmPayment.configure(bg = "SpringGreen3")

    def confirmpayment():
        try:
            if acquire_fine(me) == 0:
                raise ValueError
            elif acquire_fine(me)!=a:
                raise ValueError
            else:
                top= Toplevel(root)
                top.geometry("640x360")
                top.title("")
                top.configure(bg = "SpringGreen3")
                fine_payment(me, a)
            
                Label(top, text= "Fine Paid", font = ("lucida", 40), borderwidth = 3,wraplength = 250).place(x=150,y=80)
                top.after(2000,top.destroy)
                confirmPayment.destroy()
                finesMenuW()

        except:
            ErrorW(acquire_fine(me))


        


        
        
        
    def backToPaymentFunction():
        confirmPayment.destroy()

    headerLabel = Label(confirmPayment, text = "Please Confirm Details To Be Correct",
                    font = ("lucida", 24), borderwidth = 3, bg = "SpringGreen3", wraplength = 250)
    headerLabel.place(x = 25, y = 0, width = 300, height = 100)

    paymentDueLabel = Label(confirmPayment,text = "Payment Due",
                             font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    paymentDueLabel.place(x = 25, y = 100, width = 150, height = 50)
    fu = lambda x : 'Please return overedue amount' if acquire_fine(x[0]) is False else f'$ {acquire_fine(x[0])}'
    paymentDueEntryLabel = Label(confirmPayment,text = fu([me]),
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    paymentDueEntryLabel.place(x = 175, y = 100, width = 150, height = 50)

    exactFeeLabel = Label(confirmPayment, text = "Exact Fee Only",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    exactFeeLabel.place(x = 25, y = 150, width = 150, height = 50)

    membershipIDLabel = Label(confirmPayment, text = "Membership ID",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDLabel.place(x = 25, y = 200, width = 150, height = 50)
    membershipIDEntryLabel = Label(confirmPayment, text = me,
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    membershipIDEntryLabel.place(x = 175, y = 200, width = 150, height = 50)

    paymentDateLabel = Label(confirmPayment, text = "Payment Date",
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    paymentDateLabel.place(x = 25, y = 250, width = 150, height = 50)
    paymentDateEntryLabel = Label(confirmPayment, text = d,
                       font = ("lucida", 15), wraplength = 150, bg = "SpringGreen3")
    paymentDateEntryLabel.place(x = 175, y = 250, width = 150, height = 50)

    confirmButton = Button(confirmPayment, text = "Confirm Payment",
                       font = ("lucida", 15), wraplength = 100, command = lambda : [confirmpayment(), confirmPayment.destroy()])
    confirmButton.place(x = 50, y = 375, width = 100, height = 50)

    backButton = Button(confirmPayment, text = "Back to Payment Function",
                    font = ("lucida", 15), wraplength = 100, command = backToPaymentFunction)
    backButton.place(x = 200, y = 375, width = 100, height = 50)

def ErrorW(e):
    global noFineError
    noFineError = Toplevel()
    noFineError.title("Payment Error")
    noFineError.geometry("300x300")
    noFineError.configure(bg = "red")

    def noFineErrorBackToPaymentFunction():
        noFineError.destroy()

    headerLabel = Label(noFineError, text = "Error!",
                    font = ("lucida", 40), borderwidth = 3,wraplength = 250, bg = "red")
    headerLabel.place(x = 75, y = 40, width = 150, height = 50)
    headerLabel.configure(foreground = "yellow")

    middleLabel = Label(noFineError, text = "outstanding fine: " + str(e),
                    font = ("lucida", 15), borderwidth = 3, wraplength = 200, bg = "red")
    middleLabel.place(x = 50, y = 150, width = 200, height = 50)
    middleLabel.configure(foreground = "yellow")

    backButton = Button(noFineError, text = "Back to Payment Function",
                    font = ("lucida", 15), wraplength = 150, command = noFineErrorBackToPaymentFunction)
    backButton.place(x = 75, y = 240, width = 150, height = 40)


def reportsMenuW():
    global reportsMenu
    reportsMenu = Toplevel()
    reportsMenu.title("Reports")
    reportsMenu.geometry("1280x720")

    def reportsMenuToBookSearch():
        bookSearchW()
        reportsMenu.destroy()

    def reportsMenuToLoanedBooks():
        loanedBooksW()
        reportsMenu.destroy()

    def reportsMenuToReservedBooks():
        reservedBooksW()
        reportsMenu.destroy()

    def reportsMenuToOutstandingFines():
        outstandingFinesW()
        reportsMenu.destroy()

    def reportsMenuToMemberLoanedBooks():
        memberLoanedBooksReportW()
        reportsMenu.destroy()

    headerLabel = Label(reportsMenu, text = "Select One of the Options Below:",
                    bg = "lightblue", font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    bookSearchButton = Button(reportsMenu, text = "Book Search",
                       font = ("lucida", 18 ), command = reportsMenuToBookSearch)
    bookSearchButton.place(x = 390, y = 150, width = 500, height = 60)

    booksOnLoanButton = Button(reportsMenu, text = "Books on Loan",
                        font = ("lucida", 18), command = reportsMenuToLoanedBooks)
    booksOnLoanButton.place(x = 390, y = 250, width = 500, height = 60)

    booksOnReservationButton = Button(reportsMenu, text = "Books on Reservation",
                        font = ("lucida", 18), command = reportsMenuToReservedBooks)
    booksOnReservationButton.place(x = 390, y = 350, width = 500, height = 60)

    outstandingFinesButton = Button(reportsMenu, text = "Outstanding Fines",
                        font = ("lucida", 18), command = reportsMenuToOutstandingFines)
    outstandingFinesButton.place(x = 390, y = 450, width = 500, height = 60)

    booksOnLoanToMemberButton = Button(reportsMenu, text = "Books on Loan to Member",
                        font = ("lucida", 18), command = reportsMenuToMemberLoanedBooks)
    booksOnLoanToMemberButton.place(x = 390, y = 550, width = 500, height = 60)

    backButton = Button(reportsMenu, text = "Back To Main Menu", command= lambda : [MenuW(), reportsMenu.destroy()],
                    font = ("lucida", 16))
    backButton.place(x = 160, y = 650, width = 960, height = 50)


def bookSearchW():
    global bookSearch
    bookSearch = Toplevel()
    bookSearch.title("Reports - Book Search")
    bookSearch.geometry("1280x720")

    def bookSearchToMenu():
        reportsMenuW()
        bookSearch.destroy()

    def bookSearchToTitle():
        bookTitleW()
        bookSearch.destroy()

    def bookSearchToAuthors():
        bookAuthorsW()
        bookSearch.destroy()

    def bookSearchToisbn():
        bookISBNW()
        bookSearch.destroy()

    def bookSearchToPublisher():
        bookPublisherW()
        bookSearch.destroy()

    def bookSearchToPublicationYear():
        bookYearW()
        bookSearch.destroy()
        


    headerLabel = Label(bookSearch, text = "Search based on one of the categories below:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    titleButton = Button(bookSearch, text = "Title", font = ("lucida", 18),
                         command = bookSearchToTitle)
    titleButton.place(x = 390, y = 150, width = 500, height = 60)

    authorsButton = Button(bookSearch, text = "Authors", font = ("lucida", 18),
                           command = bookSearchToAuthors)
    authorsButton.place(x = 390, y = 250, width = 500, height = 60)

    isbnButton = Button(bookSearch, text = "ISBN", font = ("lucida", 18),
                        command = bookSearchToisbn)
    isbnButton.place(x = 390, y = 350, width = 500, height = 60)

    publisherButton = Button(bookSearch, text = "Publisher", font = ("lucida", 18),
                             command = bookSearchToPublisher)
    publisherButton.place(x = 390, y = 450, width = 500, height = 60)

    yearButton = Button(bookSearch, text = "Publication Year", font = ("lucida", 18),
                        command = bookSearchToPublicationYear)
    yearButton.place(x = 390, y = 550, width = 500, height = 60)
    
    backButton = Button(bookSearch, text = "Back To Reports Menu",
                        font = ("lucida", 20), command = bookSearchToMenu)
    backButton.place(x = 160, y = 650, width = 960, height = 50)


def bookSearchW():
    global bookSearch
    bookSearch = Toplevel()
    bookSearch.title("Reports - Book Search")
    bookSearch.geometry("1280x720")

    def bookSearchToMenu():
        reportsMenuW()
        bookSearch.destroy()

    def bookSearchToTitle():
        bookTitleW()
        bookSearch.destroy()

    def bookSearchToAuthors():
        bookAuthorsW()
        bookSearch.destroy()

    def bookSearchToisbn():
        bookISBNW()
        bookSearch.destroy()

    def bookSearchToPublisher():
        bookPublisherW()
        bookSearch.destroy()

    def bookSearchToPublicationYear():
        bookYearW()
        bookSearch.destroy()
        


    headerLabel = Label(bookSearch, text = "Search based on one of the categories below:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    titleButton = Button(bookSearch, text = "Title", font = ("lucida", 18),
                         command = bookSearchToTitle)
    titleButton.place(x = 390, y = 150, width = 500, height = 60)

    authorsButton = Button(bookSearch, text = "Authors", font = ("lucida", 18),
                           command = bookSearchToAuthors)
    authorsButton.place(x = 390, y = 250, width = 500, height = 60)

    isbnButton = Button(bookSearch, text = "ISBN", font = ("lucida", 18),
                        command = bookSearchToisbn)
    isbnButton.place(x = 390, y = 350, width = 500, height = 60)

    publisherButton = Button(bookSearch, text = "Publisher", font = ("lucida", 18),
                             command = bookSearchToPublisher)
    publisherButton.place(x = 390, y = 450, width = 500, height = 60)

    yearButton = Button(bookSearch, text = "Publication Year", font = ("lucida", 18),
                        command = bookSearchToPublicationYear)
    yearButton.place(x = 390, y = 550, width = 500, height = 60)
    
    backButton = Button(bookSearch, text = "Back To Reports Menu",
                        font = ("lucida", 20), command = bookSearchToMenu)
    backButton.place(x = 160, y = 650, width = 960, height = 50)

def bookTitleW():
    global bookTitle
    bookTitle = Toplevel()
    bookTitle.title("Book Search - Title")
    bookTitle.geometry("1280x720")

    headerLabel = Label(bookTitle, text = "Search based on Title:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    titleLabel = Label(bookTitle, text = "Title: ", font = ("lucida", 18))
    titleLabel.place(x = 300, y = 125, width = 170, height = 50)
    title = StringVar()
    titleEntry = Entry(bookTitle, textvariable = title)
    titleEntry.place(x = 470, y = 125, width = 510, height = 50)
    
    def titleToBookSearch():
        bookSearchW()
        bookTitle.destroy()

    def BookSearchToReport():
        try:
            title_name = title.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        numwords = len(title_name.split())
        if numwords > 1:
            return messagebox.showerror(title = "Error!", message = "One Word Only")
        
        bookTitle.destroy()
        ws=Tk()

        ws.title('Report on Books Searched based on title')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)

        data = []
        length = len(book_search(title_name, "title"))
        if length > 0 :
            for row in book_search(title_name, "title"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1

        #ws.mainloop()
        def ReportToMenu():
            bookSearchW()
            ws.destroy()

        #reportsMenuW()
        #loanedBooks.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)


    searchButton = Button(bookTitle, text = "Search Book", font = ("lucida", 20),
                        command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)
    backButton = Button(bookTitle, text = "Back To Search Menu",
                        font = ("lucida", 20), command = titleToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)

def bookAuthorsW():
    global bookAuthors
    bookAuthors = Toplevel()
    bookAuthors.title("Book Search - Authors")
    bookAuthors.geometry("1280x720")
        
    headerLabel = Label(bookAuthors, text = "Search based on Authors:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    authorsLabel = Label(bookAuthors, text = "Authors: ", font = ("lucida", 18))
    authorsLabel.place(x = 300, y = 125, width = 170, height = 50)
    authors = StringVar()
    authorsEntry = Entry(bookAuthors, textvariable = authors)
    authorsEntry.place(x = 470, y = 125, width = 510, height = 50)

    def authorsToBookSearch():
        bookSearchW()
        bookAuthors.destroy()

    def BookSearchToReport():
        try:
            author_name = authors.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        numwords = len(author_name.split())
        if numwords > 1:
            return messagebox.showerror(title = "Error!", message = "One Word Only")
        
        bookAuthors.destroy()
        ws=Tk()
        ws.title('Report on Books Searched based on author')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)
        data = []
        length = len(book_search(author_name, "author"))
        if length > 0 :
            for row in book_search(author_name, "author"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1
        def ReportToMenu():
            bookSearchW()
            ws.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)

    searchButton = Button(bookAuthors, text = "Search Book", font = ("lucida", 20), command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(bookAuthors, text = "Back To Search Menu",
                        font = ("lucida", 20), command = authorsToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)


def bookISBNW():
    global bookISBN
    bookISBN = Toplevel()
    bookISBN.title("Book Search - ISBN")
    bookISBN.geometry("1280x720")
    headerLabel = Label(bookISBN, text = "Search based on ISBN:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    isbnLabel = Label(bookISBN, text = "ISBN: ", font = ("lucida", 18))
    isbnLabel.place(x = 300, y = 125, width = 170, height = 50)
    isbn = StringVar()
    isbnEntry = Entry(bookISBN, textvariable = isbn)
    isbnEntry.place(x = 470, y = 125, width = 510, height = 50)

    def isbnToBookSearch():
        bookSearchW()
        bookISBN.destroy()

    def BookSearchToReport():
        try:
            isbn_no = isbn.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        numwords = len(isbn_no.split())
        if numwords > 1:
            return messagebox.showerror(title = "Error!", message = "One Word Only")
           
        bookISBN.destroy()
        ws=Tk()
        ws.title('Report on Books Searched based on ISBN')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)
        data = []
        length = len(book_search(isbn_no, "isbn"))
        if length > 0 :
            for row in book_search(isbn_no, "isbn"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1
        def ReportToMenu():
            bookSearchW()
            ws.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)

    searchButton = Button(bookISBN, text = "Search Book", font = ("lucida", 20), command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(bookISBN, text = "Back To Search Menu",
                        font = ("lucida", 20), command = isbnToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)

def bookPublisherW():
    global bookPublisher
    bookPublisher = Toplevel()
    bookPublisher.title("Book Search - Publisher")
    bookPublisher.geometry("1280x720")

    headerLabel = Label(bookPublisher, text = "Search based on Publisher:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    bookPublisherLabel = Label(bookPublisher, text = "Publisher: ", font = ("lucida", 18))
    bookPublisherLabel.place(x = 300, y = 125, width = 170, height = 50)
    publisher = StringVar()
    bookPublisherEntry = Entry(bookPublisher, textvariable = publisher)
    bookPublisherEntry.place(x = 470, y = 125, width = 510, height = 50)

    def publisherToBookSearch():
        bookSearchW()
        bookPublisher.destroy()
        
    def BookSearchToReport():
        try:
            pub = publisher.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        numwords = len(pub.split())
        if numwords > 1:
            return messagebox.showerror(title = "Error!", message = "One Word Only")
           
        bookPublisher.destroy()
        ws=Tk()
        ws.title('Report on Books Searched based on publisher')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)
        data = []
        length = len(book_search(pub, "publisher"))
        if length > 0 :
            for row in book_search(pub, "publisher"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1
        def ReportToMenu():
            bookSearchW()
            ws.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)

    searchButton = Button(bookPublisher, text = "Search Book", font = ("lucida", 20), command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(bookPublisher, text = "Back To Search Menu",
                        font = ("lucida", 20), command = publisherToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)


def bookYearW():
    global bookYear
    bookYear = Toplevel()
    bookYear.title("Book Search - Publication Year")
    bookYear.geometry("1280x720")

    headerLabel = Label(bookYear, text = "Search based on Publication Year:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    bookYearLabel = Label(bookYear, text = "Publication Year: ", font = ("lucida", 18))
    bookYearLabel.place(x = 300, y = 125, width = 170, height = 50)
    year = StringVar()
    bookYearEntry = Entry(bookYear, textvariable = year)
    bookYearEntry.place(x = 470, y = 125, width = 510, height = 50)
    bookYearEntry.delete(0, END)

    def publicationYearToBookSearch():
        bookSearchW()
        bookYear.destroy()
        
        
    def BookSearchToReport():
        try:
            pubYear = year.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
 
        bookYear.destroy()
        ws=Tk()
        ws.title('Report on Books Searched based on year published')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)
        data = []
        length = len(book_search(pubYear, "yearPublished"))
        if length > 0 :
            for row in book_search(pubYear, "yearPublished"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1
        def ReportToMenu():
            bookSearchW()
            ws.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)


    searchButton = Button(bookYear, text = "Search Book", font = ("lucida", 20), command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)


    backButton = Button(bookYear, text = "Back To Search Menu",
                        font = ("lucida", 20), command = publicationYearToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)
"""


def bookSearchW():
    global bookSearch
    bookSearch = Toplevel()
    bookSearch.title("Reports - Book Search")
    bookSearch.geometry("1280x720")

    def bookSearchToMenu():
        reportsMenuW()
        bookSearch.destroy()

    def bookSearchToTitle():
        bookTitleW()
        bookSearch.destroy()

    def bookSearchToAuthors():
        bookAuthorsW()
        bookSearch.destroy()

    def bookSearchToisbn():
        bookISBNW()
        bookSearch.destroy()

    def bookSearchToPublisher():
        bookPublisherW()
        bookSearch.destroy()

    def bookSearchToPublicationYear():
        bookYearW()
        bookSearch.destroy()
        


    headerLabel = Label(bookSearch, text = "Search based on one of the categories below:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    titleButton = Button(bookSearch, text = "Title", font = ("lucida", 18),
                         command = bookSearchToTitle)
    titleButton.place(x = 390, y = 150, width = 500, height = 60)

    authorsButton = Button(bookSearch, text = "Authors", font = ("lucida", 18),
                           command = bookSearchToAuthors)
    authorsButton.place(x = 390, y = 250, width = 500, height = 60)

    isbnButton = Button(bookSearch, text = "ISBN", font = ("lucida", 18),
                        command = bookSearchToisbn)
    isbnButton.place(x = 390, y = 350, width = 500, height = 60)

    publisherButton = Button(bookSearch, text = "Publisher", font = ("lucida", 18),
                             command = bookSearchToPublisher)
    publisherButton.place(x = 390, y = 450, width = 500, height = 60)

    yearButton = Button(bookSearch, text = "Publication Year", font = ("lucida", 18),
                        command = bookSearchToPublicationYear)
    yearButton.place(x = 390, y = 550, width = 500, height = 60)
    
    backButton = Button(bookSearch, text = "Back To Reports Menu",
                        font = ("lucida", 20), command = bookSearchToMenu)
    backButton.place(x = 160, y = 650, width = 960, height = 50)

def bookTitleW():
    global bookTitle
    bookTitle = Toplevel()
    bookTitle.title("Book Search - Title")
    bookTitle.geometry("1280x720")

    headerLabel = Label(bookTitle, text = "Search based on Title:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    titleLabel = Label(bookTitle, text = "Title: ", font = ("lucida", 18))
    titleLabel.place(x = 300, y = 125, width = 170, height = 50)
    title = StringVar()
    titleEntry = Entry(bookTitle, textvariable = title)
    titleEntry.place(x = 470, y = 125, width = 510, height = 50)
    
    def titleToBookSearch():
        bookSearchW()
        bookTitle.destroy()

    def BookSearchToReport():
        try:
            title_name = title.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        numwords = len(title_name.split())
        if numwords > 1:
            return messagebox.showerror(title = "Error!", message = "One Word Only")
        
        bookTitle.destroy()
        ws=Tk()

        ws.title('Report on Books Searched based on title')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)

        data = []
        length = len(book_search(title_name, "title"))
        if length > 0 :
            for row in book_search(title_name, "title"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1

        #ws.mainloop()
        def ReportToMenu():
            bookSearchW()
            ws.destroy()

        #reportsMenuW()
        #loanedBooks.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)


    searchButton = Button(bookTitle, text = "Search Book", font = ("lucida", 20),
                        command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)
    backButton = Button(bookTitle, text = "Back To Search Menu",
                        font = ("lucida", 20), command = titleToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)

def bookAuthorsW():
    global bookAuthors
    bookAuthors = Toplevel()
    bookAuthors.title("Book Search - Authors")
    bookAuthors.geometry("1280x720")
        
    headerLabel = Label(bookAuthors, text = "Search based on Authors:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    authorsLabel = Label(bookAuthors, text = "Authors: ", font = ("lucida", 18))
    authorsLabel.place(x = 300, y = 125, width = 170, height = 50)
    authors = StringVar()
    authorsEntry = Entry(bookAuthors, textvariable = authors)
    authorsEntry.place(x = 470, y = 125, width = 510, height = 50)

    def authorsToBookSearch():
        bookSearchW()
        bookAuthors.destroy()

    def BookSearchToReport():
        try:
            author_name = authors.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        numwords = len(author_name.split())
        if numwords > 1:
            return messagebox.showerror(title = "Error!", message = "One Word Only")
        
        bookAuthors.destroy()
        ws=Tk()
        ws.title('Report on Books Searched based on author')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)
        data = []
        length = len(book_search(author_name, "author"))
        if length > 0 :
            for row in book_search(author_name, "author"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1
        def ReportToMenu():
            bookSearchW()
            ws.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)

    searchButton = Button(bookAuthors, text = "Search Book", font = ("lucida", 20), command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(bookAuthors, text = "Back To Search Menu",
                        font = ("lucida", 20), command = authorsToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)


def bookISBNW():
    global bookISBN
    bookISBN = Toplevel()
    bookISBN.title("Book Search - ISBN")
    bookISBN.geometry("1280x720")
    headerLabel = Label(bookISBN, text = "Search based on ISBN:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    isbnLabel = Label(bookISBN, text = "ISBN: ", font = ("lucida", 18))
    isbnLabel.place(x = 300, y = 125, width = 170, height = 50)
    isbn = StringVar()
    isbnEntry = Entry(bookISBN, textvariable = isbn)
    isbnEntry.place(x = 470, y = 125, width = 510, height = 50)

    def isbnToBookSearch():
        bookSearchW()
        bookISBN.destroy()

    def BookSearchToReport():
        try:
            isbn_no = isbn.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        numwords = len(isbn_no.split())
        if numwords > 1:
            return messagebox.showerror(title = "Error!", message = "One Word Only")
           
        bookISBN.destroy()
        ws=Tk()
        ws.title('Report on Books Searched based on ISBN')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)
        data = []
        length = len(book_search(isbn_no, "isbn"))
        if length > 0 :
            for row in book_search(isbn_no, "isbn"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1
        def ReportToMenu():
            bookSearchW()
            ws.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)

    searchButton = Button(bookISBN, text = "Search Book", font = ("lucida", 20), command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(bookISBN, text = "Back To Search Menu",
                        font = ("lucida", 20), command = isbnToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)

def bookPublisherW():
    global bookPublisher
    bookPublisher = Toplevel()
    bookPublisher.title("Book Search - Publisher")
    bookPublisher.geometry("1280x720")

    headerLabel = Label(bookPublisher, text = "Search based on Publisher:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    bookPublisherLabel = Label(bookPublisher, text = "Publisher: ", font = ("lucida", 18))
    bookPublisherLabel.place(x = 300, y = 125, width = 170, height = 50)
    publisher = StringVar()
    bookPublisherEntry = Entry(bookPublisher, textvariable = publisher)
    bookPublisherEntry.place(x = 470, y = 125, width = 510, height = 50)

    def publisherToBookSearch():
        bookSearchW()
        bookPublisher.destroy()
        
    def BookSearchToReport():
        try:
            pub = publisher.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        numwords = len(pub.split())
        if numwords > 1:
            return messagebox.showerror(title = "Error!", message = "One Word Only")
           
        bookPublisher.destroy()
        ws=Tk()
        ws.title('Report on Books Searched based on publisher')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)
        data = []
        length = len(book_search(pub, "publisher"))
        if length > 0 :
            for row in book_search(pub, "publisher"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1
        def ReportToMenu():
            bookSearchW()
            ws.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)

    searchButton = Button(bookPublisher, text = "Search Book", font = ("lucida", 20), command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(bookPublisher, text = "Back To Search Menu",
                        font = ("lucida", 20), command = publisherToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)


def bookYearW():
    global bookYear
    bookYear = Toplevel()
    bookYear.title("Book Search - Publication Year")
    bookYear.geometry("1280x720")

    headerLabel = Label(bookYear, text = "Search based on Publication Year:",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    bookYearLabel = Label(bookYear, text = "Publication Year: ", font = ("lucida", 18))
    bookYearLabel.place(x = 300, y = 125, width = 170, height = 50)
    year = StringVar()
    bookYearEntry = Entry(bookYear, textvariable = year)
    bookYearEntry.place(x = 470, y = 125, width = 510, height = 50)
    bookYearEntry.delete(0, END)

    def publicationYearToBookSearch():
        bookSearchW()
        bookYear.destroy()
        
        
    def BookSearchToReport():
        try:
            pubYear = year.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
 
        bookYear.destroy()
        ws=Tk()
        ws.title('Report on Books Searched based on year published')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)
        data = []
        length = len(book_search(pubYear, "yearPublished"))
        if length > 0 :
            for row in book_search(pubYear, "yearPublished"):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1
        def ReportToMenu():
            bookSearchW()
            ws.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)


    searchButton = Button(bookYear, text = "Search Book", font = ("lucida", 20), command = BookSearchToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)


    backButton = Button(bookYear, text = "Back To Search Menu",
                        font = ("lucida", 20), command = publicationYearToBookSearch)
    backButton.place(x = 300, y = 600, width = 600, height = 80)
"""

def loanedBooksW():
    global loanedBooks
    loanedBooks = Toplevel()

    def loanReportToMenu():
        reportsMenuW()
        loanedBooks.destroy()

    def loanedBooksToReport():
        loanedBooks.destroy()
        ws=Tk()


        ws.title('Book on Loan Report')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)

        data = []
        length = len(display_loan.display_bookonloan())
        if length > 0 :
            for row in display_loan.display_bookonloan():
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1

        #ws.mainloop()
        def ReportToMenu():
            reportsMenuW()
            ws.destroy()

        #reportsMenuW()
        #loanedBooks.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)


    loanedBooks.title("Reports - Books on Loan")
    loanedBooks.geometry("1280x720")
    loanedBooks.configure(bg = "lightgreen")   
    headerLabel = Label(loanedBooks, text = "Books on Loan Report",
                    font = ("lucida", 24), borderwidth = 3, bg = "lightgreen")
    headerLabel.place(x = 160, y = 10, width = 500, height = 50)

    showButton = Button(loanedBooks, text = "Show report",
                    font = ("lucida", 20), command = loanedBooksToReport)
    showButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(loanedBooks, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = loanReportToMenu)
    backButton.place(x = 300, y = 600, width = 600, height = 80)


def reservedBooksW():
    global reservedBooks
    reservedBooks = Toplevel()

    def reservationReportToMenu():
        reportsMenuW()
        reservedBooks.destroy()

    def reserveToReport():
        reservedBooks.destroy()
        ws=Tk()


        ws.title('Book on Reservation Report')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','memberID', 'name')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=300)
        set.column("memberID",anchor=CENTER, width=150)
        set.column("name",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("memberID",text="member ID",anchor=CENTER)
        set.heading("name",text="member name",anchor=CENTER)

        data = []
        length = len(display_bookreserved.display_bookreserved())
        if length > 0 :
            for row in display_bookreserved.display_bookreserved():
                data += [list(row.values())]
                
        global count
        count = 0
        if length > 0 :
            for record in data:
                set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3]))
                count += 1

        def ReportToMenu():
            reportsMenuW()
            ws.destroy()

        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)


    reservedBooks.title("Reports - Book on Reservation")
    reservedBooks.geometry("1280x720")
    reservedBooks.configure(bg = "lightgreen")
    
    headerLabel = Label(reservedBooks, text = "Books on Reservation Report",
                    font = ("lucida", 24), borderwidth = 3, bg = "lightgreen")
    headerLabel.place(x = 160, y = 10, width = 500, height = 50)

    showButton = Button(reservedBooks, text = "Show report",
                    font = ("lucida", 20), command = reserveToReport)
    showButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(reservedBooks, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = reservationReportToMenu)
    backButton.place(x = 300, y = 600, width = 600, height = 80)

def outstandingFinesW():
    global outstandingFines
    outstandingFines = Toplevel()

    def outstandingFinesToMenu():
        reportsMenuW()
        outstandingFines.destroy()

    def outstandingFineToReport():
        outstandingFines.destroy()
        ws=Tk()
        ws.title('Book on Outstanding Fine Report')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('memberID', 'name', 'faculty', 'phone', 'email')
        set.column("#0", width=0,  stretch=NO)
        set.column("memberID",anchor=CENTER, width=150)
        set.column("name",anchor=CENTER, width=300)
        set.column("faculty",anchor=CENTER, width=150)
        set.column("phone",anchor=CENTER, width=150)
        set.column("email",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("memberID",text="Member ID",anchor=CENTER)
        set.heading("name",text="Name",anchor=CENTER)
        set.heading("faculty",text="Faculty",anchor=CENTER)
        set.heading("phone",text="Phone Number",anchor=CENTER)
        set.heading("email",text="Email Address",anchor=CENTER)

        data = []
        length = len(display_fine.display_outstandingfine())
        if length > 0 :
            for row in display_fine.display_outstandingfine():
                data += [list(row.values())]
                
        global count
        count = 0
        if length > 0 :
            for record in data:
                set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4]))
                count += 1

        def ReportToMenu():
            reportsMenuW()
            ws.destroy()

        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)

    

    outstandingFines.title("Reports - Outstanding Fines")
    outstandingFines.geometry("1280x720")
    outstandingFines.configure(bg = "lightgreen")

    headerLabel = Label(outstandingFines, text = "Members with Outstanding Fines",
                    font = ("lucida", 24), borderwidth = 3, bg = "lightgreen")
    headerLabel.place(x = 300, y = 500, width = 600, height = 80)

    showButton = Button(outstandingFines, text = "Show report",
                    font = ("lucida", 20), command = outstandingFineToReport)
    showButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(outstandingFines, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = outstandingFinesToMenu)
    backButton.place(x = 300, y = 600, width = 600, height = 80)

def memberLoanedBooksReportW():
    global booksOnLoan
    booksOnLoan = Toplevel()

    booksOnLoan.title("Reports - Books on Loan")
    booksOnLoan.geometry("1280x720")

    headerLabel = Label(booksOnLoan, text = "Books on Loan to Member",
                    font = ("lucida", 24), borderwidth = 3, relief = GROOVE)
    headerLabel.place(x = 160, y = 10, width = 960, height = 80)

    memberIDLabel = Label(booksOnLoan, text = "Membership ID: ", font = ("lucida", 18))
    memberIDLabel.place(x = 300, y = 125, width = 170, height = 50)
    memberID = StringVar()
    memberIDEntry = Entry(booksOnLoan, textvariable = memberID)
    memberIDEntry.place(x = 470, y = 125, width = 510, height = 50)


    def memberLoanedBooksToMenu():
        reportsMenuW()
        booksOnLoan.destroy()

    def memberLoanedBooksToReport():
        try:
            member_id = memberID.get()
        except:
            return messagebox.showerror(title = "Error!", message = "Missing or Incomplete fields")
        booksOnLoan.destroy()
        ws=Tk()

        ws.title('Report on Books Loaned to Member')
        ws.geometry("1280x720")
        style=ttk.Style()
        style.theme_use('clam')

        set = ttk.Treeview(ws)
        set.pack()
        set
        set['columns']= ('AccessionNo', 'title','isbn', 'publisher', 'yearpublished', 'author(s)')
        set.column("#0", width=0,  stretch=NO)
        set.column("AccessionNo",anchor=CENTER, width=150)
        set.column("title",anchor=CENTER, width=150)
        set.column("isbn",anchor=CENTER, width=150)
        set.column("publisher",anchor=CENTER, width=150)
        set.column("yearpublished",anchor=CENTER, width=150)
        set.column("author(s)",anchor=CENTER, width=300)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("AccessionNo",text="AccessionNo",anchor=CENTER)
        set.heading("title",text="title",anchor=CENTER)
        set.heading("isbn",text="isbn",anchor=CENTER)
        set.heading("publisher",text="publisher",anchor=CENTER)
        set.heading("yearpublished",text="year_published",anchor=CENTER)
        set.heading("author(s)",text="author(s)",anchor=CENTER)

        data = []
        length = len(display_bookonloan_tomember.display_bookonloan_tomember(member_id))
        if length > 0 :
            for row in display_bookonloan_tomember.display_bookonloan_tomember(member_id):
                data += [list(row.values())]
                
        global count
        count = 0
        for record in data:
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2], record[3], record[4], record[5]))
            count += 1

        #ws.mainloop()
        def ReportToMenu():
            reportsMenuW()
            ws.destroy()

        #reportsMenuW()
        #loanedBooks.destroy()
        backButton = Button(ws, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = ReportToMenu)
        backButton.place(x = 160, y = 650, width = 960, height = 50)


    searchButton = Button(booksOnLoan, text = "Search Member",
                          font = ("lucida", 20), command = memberLoanedBooksToReport)
    searchButton.place(x = 300, y = 500, width = 600, height = 80)

    backButton = Button(booksOnLoan, text = "Back To Reports Menu",
                        font = ("lucida", 20), wraplength = 150, command = memberLoanedBooksToMenu)
    backButton.place(x = 300, y = 600, width = 600, height = 80)

root.mainloop()
