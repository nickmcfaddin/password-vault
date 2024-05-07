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
    category TEXT NOT NULL,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    notes TEXT NOT NULL);               
""")

# PROGRAM FUNCTIONALITY -------------------------------------------------------------------------------------------------
window = Tk()                                                   # window initialization
window.title("Nick's Password Vault")
category = "All"

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
    window.geometry('250x150')

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
    window.geometry('1300x500')

    for widget in window.winfo_children():                      # deletes all labels, text and buttons in window
        widget.destroy()

    def categoryManager():
        window.geometry('450x450')

        for widget in window.winfo_children():                      
            widget.destroy()

        btn = Button(window, text = "<-", command = passwordVault)
        btn.grid(column = 0, pady = 20)
        
        lbl = Label(window, text = "Current Category: " + category, font = ("Helvetica", 14))
        lbl.grid(column = 1, row = 0, pady = 20)

        def swapCategory(newCategory):
            global category
            category = newCategory
            passwordVault()

        def swapCategoryToAll():
            global category
            category = "All"
            passwordVault()

        cursor.execute("SELECT DISTINCT category FROM vault ORDER BY category DESC")
        array = cursor.fetchall()

        i = 0
        if (category != "All"):
            i = 1
        
            btn = Button(window, text = "Show All Categories", command = swapCategoryToAll)
            btn.grid(column = 1, pady = 20)

        j = 0
        if(array != None):
            while j < len(array):
                lbl1 = Label(window, text = (array[j][0]), font = ("Helvetica", 10))
                lbl1.grid(column = 0, row = i+2, padx = 50)

                # need partial to take the current value of i rather than the last found
                btn = Button(window, text = "<->", command = partial(swapCategory, (array[j][0])))
                btn.grid(column = 1, row = i+2, padx = 50, pady = 10)
                
                i += 1
                j += 1

    # function to add an entry to the db
    def addEntry():
        window.geometry('250x340')

        for widget in window.winfo_children():                      
            widget.destroy()
        
        lbl = Label(window, text = "Category")
        lbl.place(x = 100, y = 10)                     

        def swapCategoryPersonal():
            global category
            category = "Personal"
            cat1.config(fg = "red")
            cat2.config(fg = "black")
            cat3.config(fg = "black")
            cat4.config(fg = "black")
            cat5.config(fg = "black")

        def swapCategorySchool():
            global category
            category = "School"
            cat1.config(fg = "black")
            cat2.config(fg = "red")
            cat3.config(fg = "black")
            cat4.config(fg = "black")
            cat5.config(fg = "black")

        def swapCategoryWork():
            global category
            category = "Work"
            cat1.config(fg = "black")
            cat2.config(fg = "black")
            cat3.config(fg = "red")
            cat4.config(fg = "black")
            cat5.config(fg = "black")

        def swapCategorySports():
            global category
            category = "Sports"
            cat1.config(fg = "black")
            cat2.config(fg = "black")
            cat3.config(fg = "black")
            cat4.config(fg = "red")
            cat5.config(fg = "black")

        def swapCategoryOther():
            global category
            category = "Other"
            cat1.config(fg = "black")
            cat2.config(fg = "black")
            cat3.config(fg = "black")
            cat4.config(fg = "black")
            cat5.config(fg = "red")

        cat1 = Button(window, text = "Personal", command = swapCategoryPersonal)
        cat1.place(x = 5, y = 35)

        cat2 = Button(window, text = "School", command = swapCategorySchool)
        cat2.place(x = 63, y = 35)

        cat3 = Button(window, text = "Work", command = swapCategoryWork)
        cat3.place(x = 113, y = 35)

        cat4 = Button(window, text = "Sports", command = swapCategorySports)
        cat4.place(x = 155, y = 35)

        cat5 = Button(window, text = "Other", command = swapCategoryOther)
        cat5.place(x = 203, y = 35)                                

        lbl1 = Label(window, text = "Website/Application")
        lbl1.place(x = 75, y = 70)

        website = Entry(window, width = 25)             
        website.place(x = 50, y = 95) 

        lbl2 = Label(window, text = "Username")
        lbl2.place(x = 100, y = 130)

        username = Entry(window, width = 25)             
        username.place(x = 50, y = 155)

        lbl3 = Label(window, text = "Password")
        lbl3.place(x = 100, y = 190)

        password = Entry(window, width = 25)             
        password.place(x = 50, y = 215)

        lbl4 = Label(window, text = "Notes")
        lbl4.place(x = 110, y = 250)

        notes = Entry(window, width = 25)             
        notes.place(x = 50, y = 275)                                         

        # saves entry to db
        def saveEntry():
            fields = """INSERT INTO vault(category, website, username, password, notes) VALUES (?, ?, ?, ?, ?)"""

            cursor.execute(fields, (category, website.get(), username.get(), password.get(), notes.get()))
            db.commit()

            passwordVault()                                                 # returns to vault after making an entry

        btn = Button(window, text = "Submit", command = saveEntry)
        btn.place(x = 100, y = 310)

    # function to remove an entry from the db
    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        passwordVault()

    lbl = Label(window, text = "Password Vault", font = ("Helvetica", 16))
    lbl.grid(column = 2)

    btn = Button(window, text = "Category: " + category, command = categoryManager)
    btn.grid(row = 1, column = 0, pady = 10)

    btn = Button(window, text = "Add Entry", command = addEntry)
    btn.grid(row = 1, column = 2,  pady = 10)

    # creates the labels for our grid of entries
    lbl = Label(window, text = "Category", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 0, padx = 80)
    lbl = Label(window, text = "Website", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 1, padx = 80)
    lbl = Label(window, text = "Username", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 2, padx = 80)
    lbl = Label(window, text = "Password", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 3, padx = 80)
    lbl = Label(window, text = "Notes", font = ("Helvetica", 12))
    lbl.grid(row = 2, column = 4, padx = 80)

    cursor.execute("SELECT * FROM vault WHERE category = (?) ORDER BY website DESC", (category,))
    if category == "All":
        cursor.execute("SELECT * FROM vault ORDER BY website DESC")
    array = cursor.fetchall()

    if(array != None):
        i = 0
        while i < len(array):
            lbl1 = Label(window, text = (array[i][1]), font = ("Helvetica", 10))
            lbl1.grid(column = 0, row = i+3)
            lbl1 = Label(window, text = (array[i][2]), font = ("Helvetica", 10))
            lbl1.grid(column = 1, row = i+3)
            lbl1 = Label(window, text = (array[i][3]), font = ("Helvetica", 10))
            lbl1.grid(column = 2, row = i+3)
            lbl1 = Label(window, text = (array[i][4]), font = ("Helvetica", 10))
            lbl1.grid(column = 3, row = i+3)
            lbl1 = Label(window, text = (array[i][5]), font = ("Helvetica", 10))
            lbl1.grid(column = 4, row = i+3)

            btn = Button(window, text = "Delete Entry", command = partial(removeEntry, array[i][0]))
            btn.grid(column = 5, row = i+3, padx = 50, pady = 10)
            
            i += 1


# START OF PROGRAM ------------------------------------------------------------------------------------------------------
cursor.execute("SELECT * FROM masterpassword")

# if we have something in our db as the master password, go direct to loginScreen, otherwise firstScreen
if cursor.fetchall():
    loginScreen()
else:
    firstScreen()

window.mainloop()
