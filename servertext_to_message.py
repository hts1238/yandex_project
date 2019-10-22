import requests
import json

data = {'user_id': 1, 'token': 'abcdefghijklmnopqrstuvwxyz123', 'sql_query': 'select * from users'}
response = requests.post('https://tim-ur.ru/yandex/makequery.php', data=data)

answer = json.loads(response.text)

print(type(answer))
print(answer)
