def send_message(from_handle, token, to_handle, text):
    import requests
    import json
    token = 'hkIi7VsViHpmlFwi5T68VgHS9'
    print(1111, from_handle, token, to_handle, text)
    data = {'from_handle': from_handle, 'token': token, 'to_handle': to_handle, 'text': text}
    response = requests.post('https://tim-ur.ru/yandex/send_message.php', data=data)

    answer = json.loads(response.text)

    # print(type(answer))
    print(answer)


# send_message(1, 2, 3, 4)
