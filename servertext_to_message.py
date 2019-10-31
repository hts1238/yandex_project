import requests
import json

data = {'handle': 'admin', 'token': 'V0z17NVgF3PQXlJQ4YuiQTZcc', 'sql_query': 'select * from users'}
response = requests.post('https://tim-ur.ru/yandex/makequery.php', data=data)

answer = json.loads(response.text)

print(type(answer))
print(answer)
