# login page with a simple Tkinter GUI
import tkinter as tk
from tkinter import messagebox


def check_login():
    user = username_var.get().strip()
    pwd = password_var.get()
    if pwd == '1133':
        messagebox.showinfo("Login", f"Login successful\nWelcome {user}!")
        status_var.set(f"Welcome {user}!")
    else:
        messagebox.showerror("Login", "Login failed")
        status_var.set("Login failed")


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

login_btn = tk.Button(frame, text="Login", width=20, command=check_login, font=("Arial", 11))
login_btn.grid(row=2, column=0, columnspan=2, pady=10)

status_var = tk.StringVar()
status_label = tk.Label(frame, textvariable=status_var, fg="green", font=("Arial", 10))
status_label.grid(row=3, column=0, columnspan=2)

# allow Enter to submit
root.bind('<Return>', lambda event: check_login())

if __name__ == "__main__":
    username_entry.focus()
    root.mainloop()