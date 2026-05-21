
#creating a banking system 




class BankAccount:
    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f'Deposited {amount}. New balance: {self.balance}')

    def withdraw(self, amount):
        if amount > self.balance:
            print('Insufficient funds')
        else:
            self.balance -= amount
            print(f'Withdrew {amount}. New balance: {self.balance}')

    def check_balance(self):
        print(f'Current balance: {self.balance}')



account_number = ''
account_holder = ''
amount = 1 
users = {
    5678: {'account_holder': 'Alice', 'balance': 1500},
    9012: {'account_holder': 'Bob', 'balance': 3000},
    1234: {'account_holder': 'Marsh', 'balance': 2300}
}

while True:
    account_number = int(input('Enter account number: '))
    
    if account_number in users:
        print('Account found')
        found_user = users[account_number]
        break
    else:
        print('Account not found')

print('--')
print('--')
print('--')

account = BankAccount(account_number, found_user['account_holder'], found_user['balance'])

account.deposit(int(input('Enter amount to deposit:')))
account.withdraw(int(input('Enter amount to withdraw:')))
account.check_balance()


