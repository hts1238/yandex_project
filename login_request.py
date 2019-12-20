def login_request(handle, password):
    """
    Выполняет авторизацию пользователя
    :param handle: логин пользователя
    :param password: пароль пользователя
    :return: ответ сервера
    """
    import requests
    import json
    from links import LOGIN_POST_QUERIES_LINK

    data = {'handle': handle, 'password': password}
    response = requests.post(LOGIN_POST_QUERIES_LINK, data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer
