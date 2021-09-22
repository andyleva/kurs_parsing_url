# Методы сбора и обработки данных из сети Интернет
# Урок 7. Selenium в Python
# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
mongo_base = client.mailru
collection = mongo_base['letters']

chrome_options = Options()

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://mail.ru/")

login = driver.find_element_by_name('login')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.ENTER)
time.sleep(2)
passw = driver.find_element_by_name('password')
passw.send_keys('NextPassword172???')
passw.send_keys(Keys.ENTER)
time.sleep(5)

articles = driver.find_element_by_class_name('llc')
print()

profile_url = articles.get_attribute('href')
driver.get(profile_url)
time.sleep(2)

but = driver.find_element_by_xpath("//span[@title='Следующее']")
print()
while but:
    lst = {}
    tema = ""
    sender = ""
    list_letter = []
    try:
        tema = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
        sender = driver.find_element_by_xpath("//span[@class='letter-contact']").text
        datemail = driver.find_element_by_xpath("//div[@class='letter__date']").text
        id = driver.find_element_by_xpath("//div[@data-id]")
        lst['Тема'] = tema
        lst['Отправитель'] = sender
        lst['Дата'] = datemail
        text_letter = id.text
        text_letter = text_letter.replace("\n", "")
        len_text = len(text_letter)
        del_text = text_letter.find("Кому: вам")
        text_letter = text_letter[(del_text + 9):len_text]
        lst['Содержание'] = text_letter.strip()
        lst['_id'] = id.id
        if collection.count_documents({'_id': lst['_id']}) == 0:
            collection.insert_one(lst)

        but.click()
        time.sleep(2)

    except Exception as e:
        # print(e)
        break

print()
client.close()
driver.close()
