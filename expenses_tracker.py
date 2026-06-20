

import tkinter as tk
from tkinter import messagebox, ttk
from db import init_db, get_user_id, add_expense as db_add_expense, get_expenses


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Expense Tracker')
        self.root.geometry('600x420')
        self.user_id = None

        top = tk.Frame(root, padx=10, pady=10)
        top.pack(fill='x')

        tk.Label(top, text='Username:').grid(row=0, column=0, sticky='w')
        self.username_var = tk.StringVar()
        tk.Entry(top, textvariable=self.username_var, width=24).grid(row=0, column=1, padx=6)
        tk.Button(top, text='Load User', command=self.load_user).grid(row=0, column=2, padx=6)

        mid = tk.LabelFrame(root, text='Add Expense', padx=10, pady=10)
        mid.pack(fill='x', padx=10, pady=8)

        tk.Label(mid, text='Amount:').grid(row=0, column=0, sticky='w')
        self.amount_var = tk.StringVar()
        tk.Entry(mid, textvariable=self.amount_var, width=20).grid(row=0, column=1, padx=6)

        tk.Label(mid, text='Note:').grid(row=1, column=0, sticky='w')
        self.note_var = tk.StringVar()
        tk.Entry(mid, textvariable=self.note_var, width=40).grid(row=1, column=1, columnspan=2, padx=6)

        tk.Button(mid, text='Add Expense', command=self.add_expense).grid(row=0, column=2, rowspan=2, padx=6)

        bottom = tk.LabelFrame(root, text='Recent Expenses', padx=10, pady=10)
        bottom.pack(fill='both', expand=True, padx=10, pady=8)

        cols = ('id', 'amount', 'note', 'created_at')
        self.tree = ttk.Treeview(bottom, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c.title())
        self.tree.column('note', width=300)
        self.tree.pack(fill='both', expand=True)

        status = tk.Frame(root)
        status.pack(fill='x')
        self.status_var = tk.StringVar(value='Not loaded')
        tk.Label(status, textvariable=self.status_var, anchor='w').pack(fill='x', padx=10, pady=6)

    def load_user(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror('User', 'Please enter a username')
            return
        uid = get_user_id(username)
        if uid is None:
            messagebox.showerror('User', 'User not found. Please create an account from the login app first.')
            return
        self.user_id = uid
        self.status_var.set(f'Loaded user {username} (id={uid})')
        self.refresh_expenses()

    def add_expense(self):
        if not self.user_id:
            messagebox.showerror('Error', 'Load a user first')
            return
        amt_s = self.amount_var.get().strip()
        note = self.note_var.get().strip()
        try:
            amt = float(amt_s)
        except ValueError:
            messagebox.showerror('Error', 'Enter a valid number for amount')
            return
        db_add_expense(self.user_id, amt, note)
        self.amount_var.set('')
        self.note_var.set('')
        self.refresh_expenses()
        messagebox.showinfo('Expense', 'Expense recorded')

    def refresh_expenses(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not self.user_id:
            self.status_var.set('No user loaded')
            return
        rows = get_expenses(self.user_id)
        total = 0.0
        for r in rows:
            self.tree.insert('', 'end', values=r)
            try:
                total += float(r[1])
            except Exception:
                pass
        self.status_var.set(f'Loaded {len(rows)} expenses — total {total:.2f}')


def main():
    init_db()
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()


def open_expense_tracker(parent=None, username=None):
    """Open the expense tracker using a Toplevel when a parent is provided.

    If `username` is given, the tracker will attempt to load that user automatically.
    """
    win = tk.Toplevel(parent) if parent else tk.Tk()
    app = ExpenseTrackerApp(win)
    if username:
        app.username_var.set(username)
        # attempt to load the user; caller may have created the user already
        try:
            app.load_user()
        except Exception:
            pass
    if not parent:
        win.mainloop()
