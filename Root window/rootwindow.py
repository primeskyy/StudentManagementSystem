# --------------------------------------------------------------
# Student Management System – MySQL + Tkinter
# --------------------------------------------------------------
from tkinter import *
from tkinter import ttk, messagebox, filedialog,simpledialog
import time
import mysql.connector
import csv
from datetime import datetime

root = Tk()

# Global DB
conn = None
mycursor = None

# --------------------------------------------------------------
# Clock
# --------------------------------------------------------------
def clock():
    datenow = time.strftime("%d/%m/%Y")
    timenow = time.strftime("%H:%M:%S")
    datetimeLabel.config(text=f'    Date - {datenow}\nTime - {timenow}')
    datetimeLabel.after(1000, clock)

# --------------------------------------------------------------
# Connect to MySQL
# --------------------------------------------------------------
def connect_database():
    def connect():
        global conn, mycursor
        try:
            conn = mysql.connector.connect(
                host=hostentry.get().strip() or 'localhost',
                user=usernameentry.get().strip(),
                password=passwordentry.get(),
                database='student_management'
            )
            mycursor = conn.cursor()
            mycursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    NAME VARCHAR(100),
                    GENDER VARCHAR(10),
                    `MOBILE NO.` VARCHAR(15),
                    EMAIL VARCHAR(100),
                    ADDRESS TEXT,
                    `D.O.B` VARCHAR(20),
                    `Added date` VARCHAR(20),
                    `Added time` VARCHAR(20)
                )
            ''')
            conn.commit()
            messagebox.showinfo('Success', 'Connected to MySQL!')
            connectwindow.destroy()
            enable_buttons()
            show_all_students()  # Show data after connect
        except Exception as e:
            messagebox.showerror('Error', f'Failed: {e}')

    # Popup window
    connectwindow = Toplevel()
    connectwindow.geometry("870x550+600+230")
    connectwindow.resizable(False, False)
    connectwindow.title("Database Connection")

    Label(connectwindow, text='Please Enter the Details for connecting to database.',
          font=('Arial', 18, 'bold'), fg="red").place(x=10, y=20)

    # Host
    Label(connectwindow, text='Host:', font=('Segoe UI', 27, 'bold')).grid(row=0, column=0, pady=80)
    hostentry = Entry(connectwindow, font=('Segoe UI', 22, 'bold'), bd=5)
    hostentry.grid(row=0, column=1, padx=60, pady=80)
    hostentry.insert(0, 'localhost')

    # User
    Label(connectwindow, text='User:', font=('Segoe UI', 27, 'bold')).grid(row=1, column=0)
    usernameentry = Entry(connectwindow, font=('Segoe UI', 22, 'bold'), bd=5)
    usernameentry.grid(row=1, column=1, padx=60)
    usernameentry.insert(0, 'pyuser')

    # Password
    Label(connectwindow, text='Pass:', font=('Segoe UI', 27, 'bold')).grid(row=2, column=0)
    passwordentry = Entry(connectwindow, font=('Segoe UI', 22, 'bold'), bd=5, show='*')
    passwordentry.grid(row=2, column=1, padx=60, pady=80)
    passwordentry.insert(0, 'MySecurePass123')

    Button(connectwindow, text="Connect", font=('Roboto Medium', 15, 'bold'),
           bg="#ffa202", cursor='hand2', fg="black", command=connect).place(x=410, y=425)

# --------------------------------------------------------------
# Add Student
# --------------------------------------------------------------
def addstudent():
    addwin = Toplevel(root)
    addwin.title("Add Student")
    addwin.geometry("500x650")
    addwin.resizable(False, False)

    entries = {}
    fields = ["NAME", "GENDER", "MOBILE NO.", "EMAIL", "ADDRESS", "D.O.B"]
    for i, field in enumerate(fields):
        Label(addwin, text=field + ":", font=('Segoe UI', 14)).grid(row=i, column=0, sticky=W, padx=15, pady=8)
        ent = Entry(addwin, font=('Segoe UI', 14), width=30)
        ent.grid(row=i, column=1, padx=15, pady=8)
        entries[field] = ent

    def save():
        try:
            now = datetime.now()
            sql = """INSERT INTO students 
                     (NAME, GENDER, `MOBILE NO.`, EMAIL, ADDRESS, `D.O.B`, `Added date`, `Added time`)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            vals = (
                entries["NAME"].get().strip(),
                entries["GENDER"].get().strip(),
                entries["MOBILE NO."].get().strip(),
                entries["EMAIL"].get().strip(),
                entries["ADDRESS"].get().strip(),
                entries["D.O.B"].get().strip(),
                now.strftime("%d/%m/%Y"),
                now.strftime("%H:%M:%S")
            )
            if not vals[0]:  # Name required
                messagebox.showwarning("Input Error", "Name is required!")
                return
            mycursor.execute(sql, vals)
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            addwin.destroy()
            show_all_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add: {e}")

    Button(addwin, text="Save Student", font=('Roboto Medium', 14, 'bold'),
           bg="#ffa202", fg="black", command=save).grid(row=6, column=0, columnspan=2, pady=20)

# --------------------------------------------------------------
# Show All Students
# --------------------------------------------------------------
def show_all_students():
    for row in studenttable.get_children():
        studenttable.delete(row)
    try:
        mycursor.execute("SELECT * FROM students")
        for row in mycursor.fetchall():
            studenttable.insert("", END, values=row)
    except:
        pass  # Ignore if not connected

#--------------------------------------------------------------
# SEARCH STUDENT
#--------------------------------------------------------------
def search_student():
    query = simpledialog.askstring("Search Student", "Enter Student ID or Name:")
    if not query:
        return
    # Clear previous table selection
    for row in studenttable.get_children():
        studenttable.delete(row)
    try:
        mycursor.execute("SELECT * FROM students WHERE ID=%s OR NAME LIKE %s", (query, f"%{query}%"))
        rows = mycursor.fetchall()
        if not rows:
            messagebox.showinfo("No Results", "No student found.")
            return
        for row in rows:
            studenttable.insert("", END, values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {e}")

#---------------------------------------------------------------
# DELETE STUDENT
#---------------------------------------------------------------

def delete_student():
    selected = studenttable.focus()
    if not selected:
        messagebox.showwarning("Select Student","Please select a student from the table!")
        return
    data = studenttable.item(selected)['values']
    confirm = messagebox.askyesno("Confirm Delete", f"Delete student '{data[1]}'?")
    if confirm:
        try:
            mycursor.execute("DELETE FROM students WHERE ID=%s", (data[0],))
            conn.commit()
            studenttable.delete(selected)
            messagebox.showinfo("Deleted","Student deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")

#---------------------------------------------------------------------
# UPDATE STUDENT
#---------------------------------------------------------------------
def update_student():
    selected = studenttable.focus()
    if not selected:
        messagebox.showwarning("Select Student", "Please select a student from the table!")
        return
    data = studenttable.item(selected)['values']
    
    updatewin = Toplevel(root)
    updatewin.title("Update Student")
    updatewin.geometry("500x650")
    updatewin.resizable(False, False)

    fields = ["NAME","GENDER","MOBILE NO.","EMAIL","ADDRESS","D.O.B"]
    entries = {}
    for i, field in enumerate(fields):
        Label(updatewin, text=field+":", font=('Segoe UI',14)).grid(row=i,column=0,sticky=W,padx=15,pady=8)
        ent = Entry(updatewin,font=('Segoe UI',14),width=30)
        ent.grid(row=i,column=1,padx=15,pady=8)
        ent.insert(0, data[i+1])  # Skip ID
        entries[field] = ent

    def save_update():
        try:
            sql = """UPDATE students SET NAME=%s, GENDER=%s, `MOBILE NO.`=%s, EMAIL=%s, ADDRESS=%s, `D.O.B`=%s
                     WHERE ID=%s"""
            vals = [entries[f].get().strip() for f in fields] + [data[0]]
            mycursor.execute(sql, vals)
            conn.commit()
            messagebox.showinfo("Success","Student updated successfully!")
            updatewin.destroy()
            show_all_students()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    Button(updatewin,text="Update Student",font=('Roboto Medium',14,'bold'),bg="#ffa202",fg="black",command=save_update).grid(row=6,column=0,columnspan=2,pady=20)
#--------------------------------------------------------------
#SHOW STUDENT
#--------------------------------------------------------------
#--------------------------------------------------------------
# SHOW STUDENT DETAILS
#--------------------------------------------------------------
def show_student():
    selected = studenttable.focus()
    if not selected:
        # No selection popup
        msgwin = Toplevel(root)
        msgwin.title("Warning")
        msgwin.geometry("400x150")
        msgwin.resizable(False, False)
        Label(msgwin, text="Please select a student from the table!", font=("Segoe UI", 14)).pack(expand=True, pady=30)
        Button(msgwin, text="OK", font=("Segoe UI", 12), command=msgwin.destroy).pack(pady=10)
        return

    data = studenttable.item(selected)['values']

    # Open a new window to show student details
    detailwin = Toplevel(root)
    detailwin.title(f"Student Details - {data[1]}")
    detailwin.geometry("500x550")
    detailwin.resizable(False, False)

    fields = ["ID", "Name", "Gender", "Mobile No.", "Email", "Address", "D.O.B", "Added Date", "Added Time"]
    for i, field in enumerate(fields):
        Label(detailwin, text=f"{field}:", font=("Segoe UI", 14, "bold")).grid(row=i, column=0, sticky=E, padx=15, pady=10)
        Label(detailwin, text=str(data[i]), font=("Segoe UI", 14)).grid(row=i, column=1, sticky=W, padx=15, pady=10)

# --------------------------------------------------------------
# Export Data to CSV (Simplest & Best)
# --------------------------------------------------------------
def export_data():
    if not conn:
        messagebox.showerror("Error", "Connect to database first!")
        return
    try:
        mycursor.execute("SELECT * FROM students")
        rows = mycursor.fetchall()
        if not rows:
            messagebox.showinfo("No Data", "No students to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Students"
        )
        if not file_path:
            return

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "NAME", "GENDER", "MOBILE NO.", "EMAIL", "ADDRESS", "D.O.B", "Added date", "Added time"])
            writer.writerows(rows)

        messagebox.showinfo("Success", f"Exported {len(rows)} student(s) to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {e}")

# --------------------------------------------------------------
# Enable buttons after connect
# --------------------------------------------------------------
def enable_buttons():
    for btn in [addstudentbutton, searchstudentbutton, deletestudentbutton,
                updatestudentbutton, showstudentbutton, exportstudentbutton]:
        btn.config(state='normal')

# --------------------------------------------------------------
# Main Window Setup
# --------------------------------------------------------------
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height-30}+0+0")
root.resizable(False, False)
root.title('Student Management System')

# Clock
datetimeLabel = Label(root, font=('Lato', 20, "bold"))
datetimeLabel.place(x=5, y=40)
titlelabel = Label(root, text="STUDENT MANAGEMENT SYSTEM", font=("Segoe UI", 33, "bold"), fg="#000753")
titlelabel.place(x=640, y=3)
clock()

# Connect button
connectbutton = Button(root, text="Connect Database", font=('Roboto Medium', 12, 'bold'),
                       bg="#ffa202", cursor='hand2', fg="black", command=connect_database)
connectbutton.place(x=1735, y=60)

# Left frame
leftframe = Frame(root)
leftframe.place(x=50, y=150, width=450, height=870)

# Logo (optional)
try:
    logoimage = PhotoImage(file='reading.png')
    logolabel = Label(leftframe, image=logoimage)
    logolabel.grid(row=0, column=0, padx=175, pady=10)
except:
    Label(leftframe, text="LOGO", font=('Arial', 30)).grid(row=0, column=0, pady=20)

# Buttons
addstudentbutton = Button(leftframe, text="  Add Student  ", font=("Roboto Medium",15,"bold"),
                          bg="#ffff00", cursor='hand2', fg="black", borderwidth=3, width=20,
                          state=DISABLED, command=addstudent)
addstudentbutton.grid(row=1, column=0, pady=40)

searchstudentbutton = Button(leftframe, text="Search Student", font=("Roboto Medium",15,"bold"),
                             bg="#ffff00", cursor='hand2', fg="black", borderwidth=3, width=20,
                             state=DISABLED,command=search_student)
searchstudentbutton.grid(row=2, column=0, pady=10)

deletestudentbutton = Button(leftframe, text="Delete Student", font=("Roboto Medium",15,"bold"),
                             bg="#ffff00", cursor='hand2', fg="black", borderwidth=3, width=20,
                             state=DISABLED,command=delete_student)
deletestudentbutton.grid(row=3, column=0, pady=40)

updatestudentbutton = Button(leftframe, text="Update Student", font=("Roboto Medium",15,"bold"),
                             bg="#ffff00", cursor='hand2', fg="black", borderwidth=3, width=20,
                             state=DISABLED,command=update_student)
updatestudentbutton.grid(row=4, column=0, pady=10)

showstudentbutton = Button(leftframe, text="Show Student", font=("Roboto Medium",15,"bold"),
                           bg="#ffff00", cursor='hand2', fg="black", borderwidth=3, width=20,
                           state=DISABLED, command=show_student)
showstudentbutton.grid(row=5, column=0, pady=40)

exportstudentbutton = Button(leftframe, text="   Export Data   ", font=("Roboto Medium",15,"bold"),
                             bg="#71ff13", cursor='hand2', fg="black", borderwidth=3, width=20,
                             state=DISABLED, command=export_data)
exportstudentbutton.grid(row=6, column=0, pady=10)

exitbutton = Button(leftframe, text="   Exit Management   ", font=("Roboto Medium",15,"bold"),
                    bg="#ff5100", cursor='hand2', fg="black", borderwidth=3, width=20,
                    command=root.destroy)
exitbutton.grid(row=7, column=0, pady=40)

# Right frame - Treeview
rightframe = Frame(root, bg="white")
rightframe.place(x=600, y=150, width=1300, height=850)

scrollbarx = Scrollbar(rightframe, orient=HORIZONTAL)
scrollbarx.pack(side=BOTTOM, fill=X)
scrollbary = Scrollbar(rightframe, orient=VERTICAL)
scrollbary.pack(side=RIGHT, fill=Y)

studenttable = ttk.Treeview(rightframe,
                            columns=("ID","NAME","GENDER","MOBILE NO.","EMAIL","ADDRESS","D.O.B","Added date","Added time"),
                            xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set)
scrollbarx.config(command=studenttable.xview)
scrollbary.config(command=studenttable.yview)

# Column settings
cols = studenttable["columns"]
headings = ["ID", "Name", "Gender", "Mobile", "Email", "Address", "D.O.B", "Added Date", "Added Time"]
widths = [60, 150, 80, 120, 200, 250, 100, 120, 100]

for col, head, w in zip(cols, headings, widths):
    studenttable.heading(col, text=head)
    studenttable.column(col, width=w, anchor=CENTER)

studenttable.config(show='headings')
studenttable.pack(fill=BOTH, expand=True)

# --------------------------------------------------------------
root.mainloop()