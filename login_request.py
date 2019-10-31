def login_request(handle, password):
    import requests
    import json

    data = {'handle': handle, 'password': password}
    response = requests.post('https://tim-ur.ru/yandex/login.php', data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer
