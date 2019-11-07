def get_senders_server(handle, token):
    """
    Функция возвращаяет юзеров, с которыми у пользователя есть переписка
    :param handle: хэндл пользователя
    :param token: токен пользователя
    :return: список юзеров
    """
    import requests
    import json

    data = {'handle': handle, 'token': token}
    response = requests.post('https://tim-ur.ru/yandex/get_message_list.php', data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer.keys() if answer else []
