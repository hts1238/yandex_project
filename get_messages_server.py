def send_message(handle, to_handle, token):
    import requests
    import json

    handle = 'admin'
    to_handle = 'vova'
    token = 'Z4yAfJl2nV7KS8rwTx2Zbj3zK'
    data = {'handle': handle, 'token': token, 'to_handle': to_handle}
    response = requests.post('https://tim-ur.ru/yandex/get_messages.php', data=data)

    answer = json.loads(response.text)

    print(type(answer))
    print(answer)


send_message(1, 2, 3)
"""
from_id, to_id, text, time
"""