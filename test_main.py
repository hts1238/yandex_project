import UiMain
from login_request import login_request
from get_messages_server import get_messages_server
import sys
import os

sys.path.insert(1, 'C:/Program Files (x86)/Messenger/')

from data import users_handles, users_names, number_of_users, dialogs, login, password

if not login or not password:
    os.system('main_login.py')
else:
    token = login_request(login, password)['token']
    with open('C:/Program Files (x86)/Messenger/data', 'w') as file:
        file.write(token)

with open('C:/Program Files (x86)/Messenger/data', 'r') as file:
    login, password, token = file.read().split()
    if not token:
        exit(0)

# with open('C:/Program Files (x86)/Messenger/data.py') as file:
#     data = file.read().split('\n')
print(123, login)
UiMain.main(users_handles, users_names, number_of_users, login, token)
