def get_message_list_server(handle, token):
    import requests
    import json

    data = {'handle': handle, 'token': token}
    response = requests.post('https://tim-ur.ru/yandex/backend/get_message_list.php', data=data)

    answer = json.loads(response.text)

    for dialog in answer:


    print(answer)


get_message_list_server('admin', 'WQo9uAu5nVXvTDrOCEuSBQxPz')
