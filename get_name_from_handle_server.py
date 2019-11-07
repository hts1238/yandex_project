def get_name_from_handle_server(handle):
    """
    Фунция форзвращия имя пользователя по его хэндлу
    :param handle: хэндл
    :return: имя порльзователя по хэндлу
    """
    import requests
    import json

    data = {'handle': handle}
    response = requests.post('https://tim-ur.ru/yandex/get_info.php', data=data)

    answer = json.loads(response.text)

    return answer['res']['name']
