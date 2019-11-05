def get_name_from_handle_server(handle):
    import requests
    import json

    data = {'handle': handle}
    response = requests.post('https://tim-ur.ru/yandex/get_info.php', data=data)

    answer = json.loads(response.text)

    return answer['res']['name']
