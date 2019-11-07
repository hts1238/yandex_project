def check_message(message):
    """
    Проверка сообщения на корректность
    :param message: сообщение, корректность которого необходимо проверить
    :return: True, если сообщение верно, False в противном случае
    """
    return 0 < len(message) < 500
