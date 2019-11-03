def synchronization_server(handle, token, senders, dialogs):
    def get_senders():
        return ['admin', 'stbru7b5qbv', 'vova', '123']

    def get_name_from_handle(handle):
        return {'admin': 'admin', 'stbru7b5qbv': 'Vladimir', 'vova': 'vova', '123': 'vlad'}[handle]

    def get_dialog(sender):
        from get_messages_server import get_messages_server
        from Message import Message
        return [Message(message[2], get_name_from_handle(message[0]), message[3]) for message in
                get_messages_server(handle, sender, token)['result']]

    new_senders = get_senders()

    something_new = bool(senders != new_senders)

    senders = new_senders

    for sender in senders:
        old_dialog = dialogs[sender]
        new_dialog = get_dialog(sender)
        if old_dialog != new_dialog:
            something_new = True
            dialogs[sender] = new_dialog

    return something_new, new_senders, dialogs
