def login_request(handle='stbru7b5qbv', password='user'):
    import requests
    import json

    data = {'handle': handle, 'password': password}
    response = requests.post('https://tim-ur.ru/yandex/login.php', data=data)

    answer = json.loads(response.text)

    print(type(answer))
    print(answer)

    return answer
