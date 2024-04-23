import requests
import psycopg2
from authorize import *

# Соединение с БД
conn = psycopg2.connect(
    dbname=name,
    user=user,
    password=password,
    host=host,
    port=port,
)

# Получение данныз из Битрикс
webhook_url = url
response = requests.get(webhook_url)
data = response.json()

# Извлеките ID
contact_id = data['ID']
contact_name = data['NAME']

# Проверьте имя контакта на наличие его в БД
cur = conn.cursor()
# ищем сред женщин
cur.execute(f"SELECT * FROM names_woman WHERE name = '{contact_name}'")
woman = cur.fetchone()
# ищем среди мужчин
cur.execute(f"SELECT * FROM names_man WHERE name = '{contact_name}'")
man = cur.fetchone()

# Анализ полученных данных
gender = None
if woman:
    gender = 'Женщина'
elif man:
    gender = 'Мужчина'

# возврат данных
if gender:
    update_url = f"{webhook_url}/update?ID={contact_id}&GENDER={gender}"
    requests.post(update_url)

cur.close()
conn.close()
