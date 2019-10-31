def refactor_message(message):
    n = 30
    ans = ''
    for i in range(len(message) // n + 1):
        ans += message[i * n:(i + 1) * n] + '\n'
    return ans.rstrip()
