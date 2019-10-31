def registration_request(email, name, handle, password):
    import requests
    import json

    data = {'email': email, 'name': name, 'handle': handle, 'password': password}
    response = requests.post('https://tim-ur.ru/yandex/register_user.php', data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer
