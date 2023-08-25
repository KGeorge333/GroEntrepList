
import subprocess
import json
import datetime
from datetime import date
from datetime import timedelta
import urllib3
from urllib3 import HTTPConnectionPool
import urllib

import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.request import urlopen

import webbrowser

import requests
from requests import Request, Response

import re

#запрос за вчеранюю дату к сервису
today = date.today()
yesterday = today - timedelta(days=1)
hcu = yesterday.strftime("%d.%m.%Y")
aurl = f"https://egr.gov.by/api/v2/egr/getAddressByPeriod/{hcu}/{hcu}"

proxies = {
"http": "http://168.90.92.65:999",
"https": "http://168.90.92.65:999",
}
# отправляем запрос к API с использованием прокси
response = requests.get(aurl, verify=False, proxies=proxies).text

obj = json.loads(response)

grodno_list = [] # перебираем каждый элемент в JSON-объекте
for item in obj: # проверяем, есть ли ключ vnp в элементе
    if "vnp" in item: # извлекаем значение vnp из элемента
        vnp = item["vnp"] # проверяем, равно ли значение vnp "Гродно"
    if vnp == "Гродно": # добавляем элемент в список
        grodno_list.append(item) # выводим список на экран

#print(grodno_list)

ngrn_list = []

for item in grodno_list:
   value1 = item.get("ngrn", None)
   if value1 is not None:
        ngrn_list.append(value1)

#print(ngrn_list)

#формируем список url
base_url = "https://egr.gov.by/egrmobile/information?" # базовый URL
url_list = [] # пустой список для URL
for item in ngrn_list: # перебираем каждый элемент в списке
    url = base_url + f"pan={item}" # формируем URL с подстановкой элемента
    url_list.append(url) # добавляем URL в список

#print(url_list) # выводим список URL на экран

url_list_str = "\n".join(url_list)

import smtplib
from email.message import EmailMessage

# создаем объект сообщения
msg = EmailMessage()
# задаем тему сообщения
msg["Subject"] = "Новые юр.лица и ИП"
# задаем отправителя сообщения
msg["From"] = "zhora_289@mail.ru"
# задаем получателя сообщения
msg["To"] = "zhora885@gmail.com"
# задаем содержание сообщения
msg.set_content(url_list_str)

# создаем объект SMTP для подключения к серверу Gmail
smtp = smtplib.SMTP("smtp.mail.ru", 587)
# активируем защищенное соединение
smtp.starttls()
# авторизуемся на сервере с помощью логина и пароля
smtp.login("zhora_289@mail.ru", "3Bwf7PrEjcr9f1P9whzf")
# отправляем сообщение
smtp.send_message(msg)
# закрываем соединение
smtp.quit()
