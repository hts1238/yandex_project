def get_messages_server(handle, to_handle, token):
    """
    Функция получения всех сообщений пользователя handle пользователю to_handle с сервера
    :param handle: хэндл пользователя
    :param to_handle: хэндл пользователя-переписчика
    :param token: токен
    :return: список сообщений
    """
    import requests
    import json
    from links import GET_MESSAGES_POST_QUERIES_LINK

    data = {'handle': handle, 'token': token, 'to_handle': to_handle}
    response = requests.post(GET_MESSAGES_POST_QUERIES_LINK, data=data)

    answer = json.loads(response.text)

    return answer