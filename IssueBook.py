from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql

# Add your own database name and password here to reflect in the code
mypass = "admin"
mydatabase = "db"

con = pymysql.connect(host="localhost", user="root",
                      password=mypass, database=mydatabase)
cur = con.cursor()

# Enter Table Names here
issueTable = "books_issued"
bookTable = "books"

# List To store all Book IDs
allBid = []


def issue():

    global issueBtn, labelFrame, lb1, inf1, inf2, quitBtn, root, Canvas1, status

    bid = inf1.get()
    issueto = inf2.get()

    issueBtn.destroy()
    labelFrame.destroy()
    lb1.destroy()
    inf1.destroy()
    inf2.destroy()

    extractBid = "select bid from "+bookTable
    try:
        cur.execute(extractBid)
        con.commit()
        for i in cur:
            allBid.append(i[0])

        if bid in allBid:
            checkAvail = "select status from "+bookTable+" where bid = '"+bid+"'"
            cur.execute(checkAvail)
            con.commit()
            for i in cur:
                check = i[0]

            if check == 'avail':
                status = True
            else:
                status = False

        else:
            messagebox.showinfo("Error", "Book ID not present")
    except:
        messagebox.showinfo("Error", "Can't fetch Book IDs")

    issueSql = "insert into "+issueTable+" values ('"+bid+"','"+issueto+"')"
    show = "select * from "+issueTable

    updateStatus = "update "+bookTable+" set status = 'issued' where bid = '"+bid+"'"
    try:
        if bid in allBid and status == True:
            cur.execute(issueSql)
            con.commit()
            cur.execute(updateStatus)
            con.commit()
            messagebox.showinfo('Success', "Book Issued Successfully")
            root.destroy()
        else:
            allBid.clear()
            messagebox.showinfo('Message', "Book Already Issued")
            root.destroy()
            return
    except:
        messagebox.showinfo(
            "Search Error", "The value entered is wrong, Try again")

    print(bid)
    print(issueto)

    allBid.clear()


def issueBook():

    global issueBtn, labelFrame, lb1, inf1, inf2, quitBtn, root, Canvas1, status

    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("700x500")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#12a4d9")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Issue Book",
                         bg='#dedad1', fg='black', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='white')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.35)

    # Book ID
    lb1 = Label(labelFrame, text="Book ID : ", bg='white', fg='black')
    lb1.place(relx=0.05, rely=0.25)

    inf1 = Entry(labelFrame, bg='#d1ccc0')
    inf1.place(relx=0.3, rely=0.25, relwidth=0.62)

    # Issued To Student name
    lb2 = Label(labelFrame, text="Issued To : ", bg='white', fg='black')
    lb2.place(relx=0.05, rely=0.45)

    inf2 = Entry(labelFrame, bg='#d1ccc0')
    inf2.place(relx=0.3, rely=0.45, relwidth=0.62)

    # Issue Button
    issueBtn = Button(root, text="Issue", bg='#d1ccc0',
                      fg='black', command=issue)
    issueBtn.place(relx=0.28, rely=0.7, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="Quit", bg='#d1ccc0',
                     fg='black', command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.7, relwidth=0.18, relheight=0.08)

    root.mainloop()
