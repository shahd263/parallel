from tkinter import  messagebox
from dbConnector import DbConnector 
from user import User

def validate_user(email, password):
        db = DbConnector()
        db.open_connection()
        cursor = db.conn.cursor()
        qry = "SELECT id FROM users WHERE email = %s AND password = %s"
        cursor.execute(qry, (email, password))
        result = cursor.fetchone()
        db.close_connection()
        return result[0] if result is not None else None
    
    

def login(email,password):
    global current_user
    current_user = validate_user(email, password)
    if current_user:
        print("Welcome to Tasks Reminder App")
    else:
        messagebox.showerror( "Error","Invalid username or password")


def logout():
    global current_user
    current_user = None
    print("Logout Successful")


def register(name,email,password):
     global current_user
     current_user=None
     db=DbConnector()
     db.open_connection()
     cursor=db.conn.cursor()
     qry="Select * from users where email = %s"
     cursor.execute(qry,(email,))
     result=cursor.fetchone()
     if result:
        messagebox.showerror("Error","There is another account with this Email")
     else:
        if not name.strip():
            messagebox.showerror("Error","Name cannot be empty.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Error","Invalid email address.")
        elif len(password) < 6:
            messagebox.showerror("Error","Password must be at least 6 characters long.")
        else:    
            User(name,email,password)
            print("Registered successfully")
            login(email,password)
     db.close_connection()
    
        
    
