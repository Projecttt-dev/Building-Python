#login page
#declare variables
username = ''
password = ''

username = input('Enter username: ')
password = input('Enter password: ')
if password == '1133':  #  actual password
    print('Login successful')
else:  print('login failed')

if password == '1133':
    print('welcome ' + username + '!')