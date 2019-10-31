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

    # sys.path.insert(1, 'C:/Program Files (x86)/Messenger/')

    from data import users_handles, users_names

    with open('data', 'r') as file:
        data = file.read().split()
        if len(data) < 3:
            login = ''
            password = ''
            token = ''
        else:
            login, password, token = data

    if login and password:
        token = login_request(login, password)['token']
    else:
        os.system('main_login.py')
        # os.startfile('main_login.pyw')

    with open('data', 'r') as file:
        data = file.read().split()
        if len(data) < 3:
            exit(1)
        else:
            login, password, token = data

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

    UiMain.main(users_handles, users_names, dialogs, login, token)


if __name__ == '__main__':
    main()