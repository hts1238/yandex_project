def refactor_message(message):
    """
    Функция преобразует сообщение в презентабельный вид
    :param message: текст сообщения, который необходимо приобразить
    :return: приображенное сообщение
    """
    n = 30
    ans = ''
    for i in range(len(message) // n + 1):
        ans += message[i * n:(i + 1) * n] + '\n'
    return ans.rstrip()
