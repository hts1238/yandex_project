def hash_password(password):
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
