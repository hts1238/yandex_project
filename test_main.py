import UiMain
import sys

sys.path.insert(1, 'C:/Program Files (x86)/Messenger/')

from data import users_handles, users_names, number_of_users, dialogs

# with open('C:/Program Files (x86)/Messenger/data.py') as file:
#     data = file.read().split('\n')
UiMain.main(users_handles, users_names, number_of_users, dialogs)
