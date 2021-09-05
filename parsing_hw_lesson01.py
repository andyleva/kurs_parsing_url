# Методы сбора и обработки данных из сети Интернет
# Урок 1. Основы клиент-серверного взаимодействия. Парсинг API
# 1) Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

# Имя пользователя github
username = "andyleva"

# url для запроса
url = f"https://api.github.com/users/{username}/repos"

# делаем запрос и возвращаем json
user_data = requests.get(url).json()

# довольно распечатать данные JSON
print("Список репозиториев GitHub :")
n = 1
for i in user_data:
    print(f"{n} : {i['name']} => {i['html_url']}")
    n += 1

# сохранить данные JSON в файл
with open('data.json', 'w') as f:
    json.dump(user_data, f)
    print("Информация json успешно сохранена в файл: data.json")



# 2) Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл

url = 'https://cloud-api.yandex.net/v1/disk'
token = '18ce83ec087cf5f75ccf9b4d39043243619a4771'

headers = {
    'Content-Type': 'application/json', \
    'Authorization': f'OAuth {token}'
}

response = requests.get(f'{url}', headers=headers)

with open('disk.json', 'w') as f:
    json.dump(response.json(), f)