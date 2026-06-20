# password generator with a simple Tkinter GUI
import random
import tkinter as tk
from tkinter import messagebox


def generate_password(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return "".join(random.choice(characters) for _ in range(length))


def open_password_generator(parent=None, callback=None):
    win = tk.Toplevel(parent) if parent else tk.Tk()
    win.title("Password Generator")
    win.geometry("400x300")
    win.resizable(False, False)

    def on_generate():
        try:
            length = int(length_entry.get())
            if length <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a positive integer for password length.")
            return

        password = generate_password(length)
        result_var.set(password)

    def on_use_password():
        password = result_var.get().strip()
        if not password:
            messagebox.showwarning("Use Password", "Generate a password first.")
            return
        if callback:
            callback(password)
            win.destroy()
            if parent:
                try:
                    parent.focus_force()
                except Exception:
                    pass
        else:
            win.clipboard_clear()
            win.clipboard_append(password)
            messagebox.showinfo("Password Copied", "Password copied to clipboard.")

    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    length_label = tk.Label(frame, text="Password Length:", font=("Arial", 12))
    length_label.grid(row=0, column=0, sticky="w")

    length_entry = tk.Entry(frame, width=10, font=("Arial", 12))
    length_entry.grid(row=0, column=1, padx=(10, 0))
    length_entry.insert(0, "12")

    generate_button = tk.Button(frame, text="Generate", command=on_generate, font=("Arial", 12), width=12)
    generate_button.grid(row=1, column=0, columnspan=2, pady=15)

    result_var = tk.StringVar()
    result_label = tk.Label(frame, text="Generated Password:", font=("Arial", 12))
    result_label.grid(row=2, column=0, sticky="w")

    result_entry = tk.Entry(frame, textvariable=result_var, width=30, font=("Arial", 12))
    result_entry.grid(row=3, column=0, columnspan=2, pady=(5, 0))

    use_button = tk.Button(frame, text="Use Password", command=on_use_password, font=("Arial", 12), width=12)
    use_button.grid(row=4, column=0, columnspan=2, pady=15)

    if not parent:
        win.mainloop()


if __name__ == "__main__":
    open_password_generator()
