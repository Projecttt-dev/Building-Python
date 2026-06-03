import tkinter as tk
from tkinter import messagebox


class BankAccount:
    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            return False, 'Invalid amount'
        self.balance += amount
        return True, f'Deposited {amount}. New balance: {self.balance}'

    def withdraw(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            return False, 'Invalid amount'
        if amount > self.balance:
            return False, 'Insufficient funds'
        self.balance -= amount
        return True, f'Withdrew {amount}. New balance: {self.balance}'

    def check_balance(self):
        return self.balance


users = {
    5678: {'account_holder': 'Alice', 'balance': 1500},
    9012: {'account_holder': 'Bob', 'balance': 3000},
    1234: {'account_holder': 'Marsh', 'balance': 2300}
}


def open_bank_window(parent=None, account_number=None):
    """Open a simple banking Tk window that prompts for account number and
    allows deposit/withdraw/check operations."""
    win = tk.Toplevel(parent) if parent else tk.Tk()
    win.title('Banking')
    win.geometry('360x220')

    frame = tk.Frame(win, padx=12, pady=12)
    frame.pack(fill='both', expand=True)

    tk.Label(frame, text='Account number:').grid(row=0, column=0, sticky='w')
    acc_var = tk.StringVar()
    acc_entry = tk.Entry(frame, textvariable=acc_var, width=20)
    acc_entry.grid(row=0, column=1, pady=6)

    status_var = tk.StringVar()
    balance_var = tk.StringVar()


    def load_account(provided_acc=None):
        if provided_acc is not None:
            acc_to_use = provided_acc
        else:
            try:
                acc_to_use = int(acc_var.get())
            except ValueError:
                messagebox.showerror('Error', 'Enter a valid numeric account number')
                return
        acc = acc_to_use
        if acc not in users:
            messagebox.showerror('Error', 'Account not found')
            return
        acc_info = users[acc]
        frame.account = BankAccount(acc, acc_info['account_holder'], acc_info['balance'])
        balance_var.set(str(frame.account.check_balance()))
        status_var.set(f"Loaded account {acc} ({frame.account.account_holder})")


    load_btn = tk.Button(frame, text='Load', command=load_account, width=10)
    load_btn.grid(row=0, column=2, padx=6)

    tk.Label(frame, text='Balance:').grid(row=1, column=0, sticky='w')
    tk.Label(frame, textvariable=balance_var, fg='blue').grid(row=1, column=1, sticky='w')

    tk.Label(frame, text='Amount:').grid(row=2, column=0, sticky='w')
    amt_var = tk.StringVar()
    amt_entry = tk.Entry(frame, textvariable=amt_var, width=20)
    amt_entry.grid(row=2, column=1, pady=6)


    def do_deposit():
        if not hasattr(frame, 'account'):
            messagebox.showerror('Error', 'Load an account first')
            return
        ok, msg = frame.account.deposit(amt_var.get())
        if not ok:
            messagebox.showerror('Error', msg)
            return
        balance_var.set(str(frame.account.check_balance()))
        messagebox.showinfo('Deposit', msg)


    def do_withdraw():
        if not hasattr(frame, 'account'):
            messagebox.showerror('Error', 'Load an account first')
            return
        ok, msg = frame.account.withdraw(amt_var.get())
        if not ok:
            messagebox.showerror('Error', msg)
            return
        balance_var.set(str(frame.account.check_balance()))
        messagebox.showinfo('Withdraw', msg)


    dep_btn = tk.Button(frame, text='Deposit', command=do_deposit, width=12)
    dep_btn.grid(row=3, column=0, pady=8)

    wdr_btn = tk.Button(frame, text='Withdraw', command=do_withdraw, width=12)
    wdr_btn.grid(row=3, column=1, pady=8)

    status_label = tk.Label(frame, textvariable=status_var, fg='green')
    status_label.grid(row=4, column=0, columnspan=3, sticky='w')

    # focus
    acc_entry.focus()

    # if caller passed an account_number, attempt to load and lock the account field
    if account_number is not None:
        try:
            acc_val = int(account_number)
        except Exception:
            acc_val = None
        if acc_val is not None and acc_val in users:
            acc_var.set(str(acc_val))
            load_account(provided_acc=acc_val)
            # disable editing since user-specific account was provided
            acc_entry.config(state='disabled')
            load_btn.config(state='disabled')

    if not parent:
        win.mainloop()


if __name__ == '__main__':
    # simple CLI fallback
    print('Running banking_system as script')
    try:
        acc = int(input('Enter account number: '))
    except ValueError:
        print('Invalid account number')
        raise SystemExit
    if acc not in users:
        print('Account not found')
        raise SystemExit
    info = users[acc]
    account = BankAccount(acc, info['account_holder'], info['balance'])
    print('Loaded', account.account_holder)
    while True:
        action = input('d)eposit w)ithdraw c)heck q)uit: ').strip().lower()
        if action == 'd':
            amt = input('Amount to deposit: ')
            ok, msg = account.deposit(amt)
            print(msg)
        elif action == 'w':
            amt = input('Amount to withdraw: ')
            ok, msg = account.withdraw(amt)
            print(msg)
        elif action == 'c':
            print('Balance:', account.check_balance())
        elif action == 'q':
            break
        else:
            print('Unknown')
