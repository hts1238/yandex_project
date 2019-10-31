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

    sys.path.insert(1, 'C:/Program Files (x86)/Messenger/')

    from data import users_handles, users_names, number_of_users, login, password

    if not login or not password:
        os.system('main_login.py')
        # os.startfile('main_login.pyw')
    else:
        token = login_request(login, password)['token']
        with open('C:/Program Files (x86)/Messenger/data', 'w') as file:
            file.write(login + '\n')
            file.write(password + '\n')
            file.write(token)

    with open('C:/Program Files (x86)/Messenger/data', 'r') as file:
        login, password, token = file.read().split()
        if not token:
            exit(0)

    # with open('C:/Program Files (x86)/Messenger/data.py') as file:
    #     data = file.read().split('\n')
    dialogs = dict()
    sender = 'stbru7b5qbv'
    dialog = get_messages_server(login, sender, token)['result']
    print(dialog)

    for message in dialog:
        if sender not in dialogs:
            dialogs[sender] = [Message(message[2], message[0], message[3])]
        else:
            dialogs[sender].append(Message(message[2], message[0], message[3]))

    UiMain.main(users_handles, users_names, dialogs, number_of_users, login, token)


if __name__ == '__main__':
    main()
