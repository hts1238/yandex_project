def get_senders_server(handle, token):
    """
    Функция возвращаяет юзеров, с которыми у пользователя есть переписка
    :param handle: хэндл пользователя
    :param token: токен пользователя
    :return: список юзеров
    """
    import requests
    import json
    from links import GET_SENDERS_POST_QUERIES_LINK

    data = {'handle': handle, 'token': token}
    response = requests.post(GET_SENDERS_POST_QUERIES_LINK, data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer.keys() if answer else []
