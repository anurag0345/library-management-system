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
bookTable = "books"


def View():

    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("700x500")

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#12a4d9")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="View Books",
                         bg='#d1ccc0', fg='black', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='white')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.38)
    y = 0.3

    Label(labelFrame, text="%-10s%-60s%-40s%-10s" % ('BID', 'Title',
          'Author', 'Status'), bg='white', fg='black').place(relx=0.07, rely=0.1)
    Label(labelFrame, text="-------------------------------------------------------------------------------------",
          bg='white', fg='black').place(relx=0.05, rely=0.2)
    getBooks = "select * from "+bookTable
    try:
        cur.execute(getBooks)
        con.commit()
        for i in cur:
            Label(labelFrame, text="%-10s%-50s%-40s%-20s" %
                  (i[0], i[1], i[2], i[3]), bg='white', fg='black').place(relx=0.07, rely=y)
            y += 0.1
    except:
        messagebox.showinfo("Failed to fetch files from database")

    quitBtn = Button(root, text="Quit", bg='#f7f1e3',
                     fg='black', command=root.destroy)
    quitBtn.place(relx=0.4, rely=0.78, relwidth=0.18, relheight=0.08)

    root.mainloop()
