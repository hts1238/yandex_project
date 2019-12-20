def get_name_from_handle_server(handle):
    """
    Фунция форзвращия имя пользователя по его хэндлу
    :param handle: хэндл
    :return: имя пользователя по хэндлу
    """
    import requests
    import json
    from links import GET_NAME_FROM_HANDLE_POST_QUERIES_LINK

    data = {'handle': handle}
    response = requests.post(GET_NAME_FROM_HANDLE_POST_QUERIES_LINK, data=data)

    answer = json.loads(response.text)

    return answer['res']['name']
