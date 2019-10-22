import UiMain
import sys

sys.path.insert(1, 'C:/Program Files (x86)/Messenger/')

from data import users_names, number_of_users, dialogs

# with open('C:/Program Files (x86)/Messenger/data.messenger') as file:
#     data = file.read().split('\n')
UiMain.main(users_names, number_of_users, dialogs)
