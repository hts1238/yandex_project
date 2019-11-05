def synchronization_server(handle, token, senders, dialogs, names_of_users):
    def get_senders():
        from get_senders_server import get_senders_server
        return get_senders_server(handle, token)

    def get_name_from_handle(handle):
        return names_of_users[handle]

    def get_dialog(sender):
        from get_messages_server import get_messages_server
        from Message import Message
        return [Message(message[2], get_name_from_handle(message[0]), message[3]) for message in
                get_messages_server(handle, sender, token)['result']]

    new_senders = get_senders()

    something_new = bool(set(senders) != set(new_senders))
    senders = new_senders
    for sender in senders:
        old_dialog = dialogs[sender] if sender in dialogs else []
        new_dialog = get_dialog(sender)
        if not old_dialog or old_dialog[-1] != new_dialog[-1]:
            something_new = True
            dialogs[sender] = new_dialog

    return something_new, new_senders, dialogs
