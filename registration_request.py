def registration_request(email, name, handle, password):
    """
    Веполняет регистрацию пользователя через сервер
    :param email: адрес электронной почты нового пользователя
    :param name: имя нового пользователя
    :param handle: хэндл нового пользователя
    :param password: пароль нового пользователя
    :return: результат регистрации
    """
    import requests
    import json

    data = {'email': email, 'name': name, 'handle': handle, 'password': password}
    response = requests.post('https://tim-ur.ru/yandex/register_user.php', data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer
