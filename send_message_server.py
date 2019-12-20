def send_message_server(from_handle, token, to_handle, text):
    """
    Отправка сообщения на сервер
    :param from_handle: хэндл пользователя-отправителя
    :param token: токен пользователя-отправителя
    :param to_handle: хэндл пользователя-получателя
    :param text: текст сообщения
    :return: None
    """
    import requests
    import json
    from links import SEND_MESSAGE_POST_QUERIES_LINK

    if not text:
        return
    print(from_handle, token, to_handle, text.rstrip())
    data = {'from_handle': from_handle, 'token': token, 'to_handle': to_handle, 'text': text}
    response = requests.post(SENG_MESSAGE_POST_QUERIES_LINK, data=data)

    answer = json.loads(response.text)

    print(answer)
