# IMPORT STATEMENTS -----------------------------------------------------------------------------------------------------
import sqlite3, hashlib
from tkinter import *
from functools import partial

# DB INITIALIZATION -----------------------------------------------------------------------------------------------------
with sqlite3.connect("password-vault.db") as db:                # initialize db
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
    id INTEGER PRIMARY KEY,
    password TEXT NOT NULL);               
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
    id INTEGER PRIMARY KEY,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    notes TEXT NOT NULL);               
""")

# PROGRAM FUNCTIONALITY -------------------------------------------------------------------------------------------------
window = Tk()                                                   # window initialization
window.title("Nick's Password Vault")

# encodes our passwords
def hashPassword(input):
    hash = hashlib.md5(input)                                   # takes text and turns it into md5 hash
    hash = hash.hexdigest()                                     # turns hash back to something we can use

    return hash

# initial screen when the user accesses program for the first time
def firstScreen():
    window.geometry('250x150')

    lbl = Label(window, text = "Create Master Password")
    lbl.config(anchor = CENTER)
    lbl.pack()                          

    txt = Entry(window, width = 25)             
    txt.pack()
    txt.focus()                                                 # cursor automatically goes to here

    lbl1 = Label(window, text = "Re-enter Master Password")
    lbl1.pack()

    txt1 = Entry(window, width = 25)             
    txt1.pack()

    lbl2 = Label(window)                                        # passwords not matching label
    lbl2.pack()                                             

    # saves master password and hashes it, sends to db
    def saveMasterPassword():
        if txt.get() == txt1.get():
            hashedPassword = hashPassword(txt.get().encode('utf-8'))    # give our hashPassword function a utf-8 encoded string

            typedPassword = """INSERT INTO masterpassword(password) VALUES (?)"""

            cursor.execute(typedPassword, [(hashedPassword)])   # executes above line with hashedPassword as the ?
            db.commit()

            passwordVault()
        else:
            lbl2.config(text = "Passwords do not match")

    btn = Button(window, text = "Submit", command = saveMasterPassword)
    btn.pack(pady = 10)

# login screen that appears each time the user accesses the application
def loginScreen():
    window.geometry('250x100')

    lbl = Label(window, text = "Enter Master Password")
    lbl.config(anchor = CENTER)
    lbl.pack()

    txt = Entry(window, width = 25, show = "*")             
    txt.pack()
    txt.focus()                                            

    lbl1 = Label(window)                                        # correct/incorrect password label
    lbl1.pack()

    def getMasterPassword():
        checkHashedPassword = hashPassword(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()                                # anytime we use cursor.fetchall, cursor.execute has to be right before
    
    # checks for correct master pass
    def checkPassword():
        match = getMasterPassword()

        if match:
            passwordVault()
        else:
            txt.delete(0, 'end')                                # clears text box
            lbl1.config(text = "Incorrect password.")

    btn = Button(window, text = "Submit", command = checkPassword)
    btn.pack(pady = 10)

# main password vault
def passwordVault():
    window.geometry('1050x500')

    for widget in window.winfo_children():                      # deletes all labels, text and buttons in window
        widget.destroy()

    # function to add an entry to the db
    def addEntry():
        window.geometry('250x300')

        for widget in window.winfo_children():                      
            widget.destroy()

        lbl = Label(window, text = "Website/Application")
        lbl.config(anchor = CENTER)
        lbl.pack()                          

        website = Entry(window, width = 25)             
        website.pack()
        website.focus()                                         

        lbl1 = Label(window, text = "Username")
        lbl1.pack()

        username = Entry(window, width = 25)             
        username.pack()

        lbl2 = Label(window, text = "Password")
        lbl2.pack()

        password = Entry(window, width = 25)             
        password.pack()

        lbl3 = Label(window, text = "Notes")
        lbl3.pack()

        notes = Entry(window, width = 25)             
        notes.pack()                                            

        # saves entry to db
        def saveEntry():
            fields = """INSERT INTO vault(website, username, password, notes) VALUES (?, ?, ?, ?)"""

            cursor.execute(fields, (website.get(), username.get(), password.get(), notes.get()))
            db.commit()

            passwordVault()                                                 # returns to vault after making an entry

        btn = Button(window, text = "Submit", command = saveEntry)
        btn.pack(pady = 10)

    # function to remove an entry from the db
    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        passwordVault()

    lbl = Label(window, text = "Password Vault", font = ("Helvetica", 16))
    lbl.grid(column = 2)

    btn = Button(window, text = "Add Entry", command = addEntry)
    btn.grid(column = 2,  pady = 10)

    # creates the labels for our grid of entries
    lbl = Label(window, text = "Website", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 0, padx = 80)
    lbl = Label(window, text = "Username", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 1, padx = 80)
    lbl = Label(window, text = "Password", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 2, padx = 80)
    lbl = Label(window, text = "Notes", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 3, padx = 80)

    cursor.execute("SELECT * FROM vault")
    count = cursor.fetchall()
    if(count != None):
        i = 0
        while i < len(count):
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            lbl1 = Label(window, text = (array[i][1]), font = ("Helvetica", 10))
            lbl1.grid(column = 0, row = i+3)
            lbl1 = Label(window, text = (array[i][2]), font = ("Helvetica", 10))
            lbl1.grid(column = 1, row = i+3)
            lbl1 = Label(window, text = (array[i][3]), font = ("Helvetica", 10))
            lbl1.grid(column = 2, row = i+3)
            lbl1 = Label(window, text = (array[i][4]), font = ("Helvetica", 10))
            lbl1.grid(column = 3, row = i+3)

            # need partial to take the current value of i rather than the last found
            btn = Button(window, text = "Delete Entry", command = partial(removeEntry, array[i][0]))
            btn.grid(column = 4, row = i+3, padx = 50, pady = 10)
            
            i += 1


# START OF PROGRAM ------------------------------------------------------------------------------------------------------
cursor.execute("SELECT * FROM masterpassword")

# if we have something in our db as the master password, go direct to loginScreen, otherwise firstScreen
if cursor.fetchall():
    loginScreen()
else:
    firstScreen()

window.mainloop()