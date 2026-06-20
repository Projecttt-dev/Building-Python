# login page with a simple Tkinter GUI
import tkinter as tk
from tkinter import messagebox
from db import init_db, create_user, authenticate
import banking_system
import password_generator


def check_login():
    user = username_var.get().strip()
    pwd = password_var.get()
    if not user or not pwd:
        messagebox.showerror("Login", "Please enter username and password")
        return
    if authenticate(user, pwd):
        messagebox.showinfo("Login", f"Login successful\nWelcome {user}!")
        status_var.set(f"Welcome {user}!")
        # try to find a matching bank account for this username
        matched_acc = None
        for acc_num, info in banking_system.users.items():
            if str(info.get('account_holder')).lower() == user.lower():
                matched_acc = acc_num
                break
        # open banking window, pass account if found so it loads automatically
        try:
            banking_system.open_bank_window(root, account_number=matched_acc)
        except Exception as e:
            messagebox.showerror('Banking', f'Unable to open banking window: {e}')
    else:
        messagebox.showerror("Login", "Invalid username or password")
        status_var.set("Login failed")


def fill_generated_password(pw):
    password_var.set(pw)


def signup():
    user = username_var.get().strip()
    pwd = password_var.get()
    if not user or not pwd:
        messagebox.showerror("Signup", "Please enter username and password")
        return
    if create_user(user, pwd):
        messagebox.showinfo("Signup", f"Account created!\nWelcome {user}!")
        status_var.set(f"Account created for {user}!")
        username_var.set("")
        password_var.set("")
    else:
        messagebox.showerror("Signup", "Username already exists")
        status_var.set("Signup failed")


root = tk.Tk()
root.title("Login")
root.geometry("350x180")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=15)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Username:", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
username_var = tk.StringVar()
username_entry = tk.Entry(frame, textvariable=username_var, width=25, font=("Arial", 11))
username_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Password:", font=("Arial", 11)).grid(row=1, column=0, sticky="w")
password_var = tk.StringVar()
password_entry = tk.Entry(frame, textvariable=password_var, show="*", width=25, font=("Arial", 11))
password_entry.grid(row=1, column=1, pady=5)

login_btn = tk.Button(frame, text="Login", width=15, command=check_login, font=("Arial", 11))
login_btn.grid(row=2, column=0, pady=10, padx=5)

signup_btn = tk.Button(frame, text="Sign Up", width=15, command=signup, font=("Arial", 11))
signup_btn.grid(row=2, column=1, pady=10, padx=5)

password_gen_btn = tk.Button(frame, text="Generate Password", width=15, command=lambda: password_generator.open_password_generator(root, callback=fill_generated_password), font=("Arial", 11))
password_gen_btn.grid(row=3, column=0, pady=5, padx=5, columnspan=2)

status_var = tk.StringVar()
status_label = tk.Label(frame, textvariable=status_var, fg="green", font=("Arial", 10))
status_label.grid(row=4, column=0, columnspan=2)

# allow Enter to submit
root.bind('<Return>', lambda event: check_login())

if __name__ == "__main__":
    init_db()
    username_entry.focus()
    root.mainloop()