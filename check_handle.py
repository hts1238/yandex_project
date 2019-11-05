def check_handle(handle):
    import requests
    import json

    data = {'handle': handle}
    response = requests.post('https://tim-ur.ru/yandex/check_handle.php', data=data)

    answer = json.loads(response.text)

    return answer['res']
