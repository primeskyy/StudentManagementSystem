from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image


def login():
    if usernameentry.get() == "" or passwordentry.get() == "":
        messagebox.showerror("Error", "Fields can't be empty.")
    elif usernameentry.get() == 'Akash' and passwordentry.get() == '1234':
        messagebox.showinfo("Success", "Welcome Akash!")
        loginwindow.destroy()
        import rootwindow

    else:
        messagebox.showerror("Error", "Please enter correct credentials.")


loginwindow = Tk()

# Fullscreen (minus title bar)
screen_width = loginwindow.winfo_screenwidth()
screen_height = loginwindow.winfo_screenheight()
loginwindow.geometry(f"{screen_width}x{screen_height-30}+0+0")
loginwindow.title('Login Window of Student Management System.')
loginwindow.resizable(False, False)

# Background image
original_image = Image.open('3409297.jpg')
resized_image = original_image.resize((screen_width, screen_height-30), Image.Resampling.LANCZOS)
backgroundImage = ImageTk.PhotoImage(resized_image)
bgLabel = Label(loginwindow, image=backgroundImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

# Login frame
loginframe = Frame(loginwindow, bg="#d8d9d9", bd=2, relief=RIDGE)
loginframe.place(x=725, y=225)

# Logo & Title
logoimage = PhotoImage(file='graduate.png')
logolabel = Label(loginframe, image=logoimage)
logolabel.grid(row=0, column=0, columnspan=2, pady=50)
titlelabel = Label(loginwindow,text="Login Portal",font=("Poppins",15,"bold"),fg="#000753")
titlelabel.place(x=915,y=340)


# Username
usernameimage = PhotoImage(file="user.png")
usernamelabel = Label(loginframe, image=usernameimage, text='  Username : ', compound=LEFT, font=('Segoe UI', 20, 'bold'))
usernamelabel.grid(row=1, column=0, pady=10, padx=20)
usernameentry = Entry(loginframe, font=('Segoe UI', 15, 'bold'), bd=5)
usernameentry.grid(row=1, column=1, pady=10, padx=20)

# Password
passwordimage = PhotoImage(file="padlock.png")
passwordlabel = Label(loginframe, image=passwordimage, text='  Password : ', compound=LEFT, font=('Segoe UI', 20, 'bold'))
passwordlabel.grid(row=2, column=0, pady=10, padx=20)
passwordentry = Entry(loginframe, font=('Segoe UI', 15, 'bold'), bd=5, show='*')
passwordentry.grid(row=2, column=1, pady=10, padx=20)

# Login button
loginbutton = Button(loginframe, text="LOGIN", font=('Roboto Medium', 10, 'bold'), bg="#47d664", cursor='hand2', command=login)
loginbutton.grid(row=3, column=0, columnspan=2, pady=40, padx=10)

loginwindow.mainloop()