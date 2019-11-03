"""
█   █ ███ ███ ███ ███ █  █ ████ ███ ████
██ ██ █   █   █   █   ██ █ █    █   █  █
█ █ █ ███ ███ ███ ███ █ ██ █ ██ ███ ████
█   █ █     █   █ █   █  █ █  █ █   █ █
█   █ ███ ███ ███ ███ █  █ ████ ███ █ █
"""


def main():
    import UiMain
    from Message import Message
    from login_request import login_request
    from get_messages_server import get_messages_server
    import sys
    import os
    import csv

    # sys.path.insert(1, 'C:/Program Files (x86)/Messenger/')

    from data import users_handles, users_names

    with open('data.csv', encoding="utf8") as file:
        reader = list(csv.reader(file, delimiter=';', quotechar='"'))
        reader = reader[0] if reader else []
        data = reader
        if len(data) < 4:
            login = ''
            password = ''
            token = ''
            remember = False
        else:
            login, password, token, remember = data

    if login and password:
        token = login_request(login, password)['token']
    else:
        os.system('main_login.py')
        # os.startfile('main_login.pyw')

    with open('data.csv', encoding="utf8") as file:
        reader = list(csv.reader(file, delimiter=';', quotechar='"'))
        reader = reader[0] if reader else []
        data = reader
        print(data)
        if len(data) < 4:
            exit(228)
        else:
            login, password, token, remember = data

    # with open('C:/Program Files (x86)/Messenger/data.py') as file:
    #     data = file.read().split('\n')

    dialogs = dict()
    for sender in users_handles:
        dialog = get_messages_server(login, sender, token)['result']
        for message in dialog:
            if sender not in dialogs:
                dialogs[sender] = [Message(message[2], users_names[message[0]], message[3])]
            else:
                dialogs[sender].append(Message(message[2], users_names[message[0]], message[3]))
        if not dialog:
            dialogs[sender] = []

    UiMain.main(users_handles, users_names, dialogs, login, token, remember)


if __name__ == '__main__':
    main()
