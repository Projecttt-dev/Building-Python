#expenses tracker

balance = 20000000.00
def add_expense(amount):
    global balance
    balance -= amount
    print(f"Expense of {amount} added. Current balance: {balance}")
def add_income(amount):
    global balance
    balance += amount
    print(f"Income of {amount} added. Current balance: {balance}")

while True:
    action = input("Enter 'expense' to add an expense or 'income' to add income (or 'exit' to quit): ")
    if action == 'expense':
        amount = float(input("Enter expense amount: "))
        add_expense(amount)
    elif action == 'income':
        amount = float(input("Enter income amount: "))
        add_income(amount)
    elif action == 'exit':
        print("Exiting the tracker. Final balance: ", balance)
        break
    else:
        print("Invalid input. Please enter 'expense', 'income', or 'exit'.")

if balance < 120000.00:
    print("Warning: Your balance is below 120,000.00. Consider reviewing your expenses.")
else:
    print("Your balance is healthy. Keep up the good work!")           