def check_password(password):
    """
    Проверка пароля на корректность
    :param password: пароль, корректность которого необходимо проверить
    :return: True, если пароль проходит проверку безопасности, False в противном случае
    """
    return 5 <= len(password) <= 30 and \
           all(_ in 'qwertyupasdifghjkzxcvbnmQWERTYUPASDIFGHJKZXCVBNM0123456789' for _ in password)
