def registration_request(email='123@yandex.ru', name='Vladimir', handle='stbru7b5qbv', password='user'):
    import requests
    import json

    data = {'email': email, 'name': name, 'handle': handle, 'password': password}
    response = requests.post('https://tim-ur.ru/yandex/register_user.php', data=data)

    answer = json.loads(response.text)

    print(type(answer))
    print(answer)

    return answer
