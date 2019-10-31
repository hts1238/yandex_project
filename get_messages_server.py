def get_messages_server(handle, to_handle, token):
    import requests
    import json

    data = {'handle': handle, 'token': token, 'to_handle': to_handle}
    response = requests.post('https://tim-ur.ru/yandex/get_messages.php', data=data)

    answer = json.loads(response.text)

    return answer
