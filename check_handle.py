def check_handle(handle):
    """
    Функция проверки на присутствие хэдла в базе зарегистрированных пользователей
    :param handle: хэндл, который необходимо проверить
    :return: 0 если пользователь зарегистрирован, 1 в противном случае
    """
    import requests
    import json

    data = {'handle': handle}
    response = requests.post('https://tim-ur.ru/yandex/check_handle.php', data=data)

    answer = json.loads(response.text)

    return answer['res']
