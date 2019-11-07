def hash_password(password):
    """
    Функция хеширует переданный пароль с помощью технологнии bcrypt
    :param password: пароль, который необходимо хэшировать
    :return: хэш пароля
    """
    import bcrypt

    password = bytes(password, encoding='utf8')

    salt = bcrypt.gensalt(rounds=12)

    hashed = bcrypt.hashpw(password, salt)

    return hashed
    # salt = bcrypt.gensalt(rounds=31)
    # hashed = bcrypt.hashpw(password, salt)
    #
    # print(f'bcrypt:\n{hashed}')
    # print(bcrypt.checkpw(password, hashed))
