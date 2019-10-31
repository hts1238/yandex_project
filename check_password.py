def check_password(password):
    return 5 <= len(password) <= 30 and\
           all(_ in 'qwertyupasdifghjkzxcvbnmQWERTYUPASDIFGHJKZXCVBNM0123456789' for _ in password)
