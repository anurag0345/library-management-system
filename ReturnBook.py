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
issueTable = "books_issued"  # Issue Table
bookTable = "books"  # Book Table


allBid = []  # List To store all Book IDs


def returnn():

    global SubmitBtn, labelFrame, lb1, bookInfo1, quitBtn, root, Canvas1, status

    bid = bookInfo1.get()

    extractBid = "select bid from "+issueTable
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

            if check == 'issued':
                status = True
            else:
                status = False

        else:
            messagebox.showinfo("Error", "Book ID not present")
    except:
        messagebox.showinfo("Error", "Can't fetch Book IDs")

    issueSql = "delete from "+issueTable+" where bid = '"+bid+"'"

    print(bid in allBid)
    print(status)
    updateStatus = "update "+bookTable+" set status = 'avail' where bid = '"+bid+"'"
    try:
        if bid in allBid and status == True:
            cur.execute(issueSql)
            con.commit()
            cur.execute(updateStatus)
            con.commit()
            messagebox.showinfo('Success', "Book Returned Successfully")
        else:
            allBid.clear()
            messagebox.showinfo('Message', "Please check the book ID")
            root.destroy()
            return
    except:
        messagebox.showinfo(
            "Search Error", "The value entered is wrong, Try again")

    allBid.clear()
    root.destroy()


def returnBook():

    global bookInfo1, SubmitBtn, quitBtn, Canvas1, con, cur, root, labelFrame, lb1

    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("700x500")

    Canvas1 = Canvas(root)

    Canvas1.config(bg="#12a4d9")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Return Book",
                         bg='#dedad1', fg='black', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='white')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.35)

    # Book ID to Delete
    lb1 = Label(labelFrame, text="Book ID : ", bg='white', fg='black')
    lb1.place(relx=0.05, rely=0.45)

    bookInfo1 = Entry(labelFrame, bg='#d1ccc0')
    bookInfo1.place(relx=0.3, rely=0.45, relwidth=0.62)

    # Submit Button
    SubmitBtn = Button(root, text="Return", bg='#d1ccc0',
                       fg='black', command=returnn)
    SubmitBtn.place(relx=0.28, rely=0.7, relwidth=0.18, relheight=0.08)

    quitBtn = Button(root, text="Quit", bg='#d1ccc0',
                     fg='black', command=root.destroy)
    quitBtn.place(relx=0.53, rely=0.7, relwidth=0.18, relheight=0.08)

    root.mainloop()
