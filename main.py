"""
█   █ ███ ███ ███ ███ █  █ ████ ███ ████
██ ██ █   █   █   █   ██ █ █    █   █  █
█ █ █ ███ ███ ███ ███ █ ██ █ ██ ███ ████
█   █ █     █   █ █   █  █ █  █ █   █ █
█   █ ███ ███ ███ ███ █  █ ████ ███ █ █
"""

from files import *


def main():
    """
    Функция запуска оконного приложения Messenger
    :return: None
    """
    import sys
    import os
    import csv

    import UiMain
    from Message import Message
    from login_request import login_request
    from get_messages_server import get_messages_server
    from get_senders_server import get_senders_server
    from get_name_from_handle_server import get_name_from_handle_server

    # sys.path.insert(1, 'C:/Program Files (x86)/Messenger/')

    try:
        with open(DATA, encoding="utf8") as file:
            reader = list(csv.reader(file, delimiter=';', quotechar='"'))
            reader = reader[0] if reader else []
            try:
                login, password, token, remember = reader
            except ValueError:
                login, password, token, remember = '', '', '', False
    except FileNotFoundError:
        with open(DATA, 'w+', encoding="utf8") as file:
            login = ''
            password = ''
            token = ''
            remember = False

    if login and password:
        token = login_request(login, password)['token']
    else:
        os.system(LOGIN_PY)
        # os.startfile('main_login.pyw')

    with open(DATA, encoding="utf8") as file:
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

    users_handles = list(get_senders_server(login, token))
    if login not in users_handles:
        users_handles.append(login)

    users_names = dict()

    for handle in users_handles:
        users_names[handle] = get_name_from_handle_server(handle)

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
