def send_message_server(from_handle, token, to_handle, text):
    import requests
    import json

    if not text:
        return
    print(from_handle, token, to_handle, text.rstrip())
    data = {'from_handle': from_handle, 'token': token, 'to_handle': to_handle, 'text': text}
    response = requests.post('https://tim-ur.ru/yandex/send_message.php', data=data)

    answer = json.loads(response.text)

    print(answer)
