def get_name_from_handle_server(handle):
    '''
    import requests
    import json

    data = {'handle': handle}
    response = requests.post('https://tim-ur.ru/yandex/get_messages.php', data=data)

    answer = json.loads(response.text)

    return answer['name']
    '''
    return {'admin': 'admin', 'stbru7b5qbv': 'Vladimir', 'vova': 'vova', '123': 'vlad', 'tim': 'tim'}[handle]
