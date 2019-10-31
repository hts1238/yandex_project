from time import time

start = time()

import hashlib

password = '123456'
print('md5:\n' + hashlib.md5(f"{password}".encode('utf-8')).hexdigest())
print(time() - start)
print('sha512:\n' + hashlib.sha512(f"{password}".encode('utf-8')).hexdigest())
print('blake2b:\n' + hashlib.blake2b(f"{password}".encode('utf-8')).hexdigest())
start = time()
"""





"""
import bcrypt

password = bytes(password, encoding='utf8')

salt = bcrypt.gensalt(rounds=12)
# salt = bcrypt.gensalt(rounds=31)
hashed = bcrypt.hashpw(password, salt)

print(f'bcrypt:\n{hashed}')
print(time() - start)
print(bcrypt.checkpw(password, hashed))
print(bcrypt.checkpw(password, b'$2b$12$rFBzeAq5f46FsC2rhVFHnO14C6gCTT2v46I6pP0HDXECof0Mlq2v6'))
