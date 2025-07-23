from tkinter import *
import tkinter as tk
from db_comms import *
from tkinter import messagebox

app = tk.Tk()
app.title('CRMLite - Local DB')

tk.Label(app,text='Συνδεθείτε:').pack()

tk.Label(app,text='Username').pack()
user_entry = Entry(app)
user_entry.pack()

tk.Label(app,text='Password:').pack()
passw_entry = Entry(app,show='•	')
passw_entry.pack()

def clear_app():
    for widget in app.winfo_children():
        widget.forget()

def start_auth():
    global username
    username = user_entry.get()
    password = passw_entry.get()
    auth_check,u_exist = auth(username,password)
    if u_exist == True:
        if auth_check == True:
            home()
        else:
            messagebox.showerror('Σφάλμα σύνδεσης','Ο κωδικός πρόσβασης είναι λάθος')
    else:
        messagebox.showerror('Σφάλμα σύνδεσης!','Δεν υπάρχει χρήστης με αυτό το όνομα!')

tk.Button(app,text='Σύνδεση',command=start_auth).pack()

def home():
    clear_app()
    tk.Label(app,text=f"Καλωσόρισες {username}").pack()





app.mainloop()

