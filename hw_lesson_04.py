# Урок 4. Парсинг HTML. XPath
# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

from lxml import html
import requests
from pprint import pprint
from datetime import date


def parse_news_lenta(params, headers):
    now = date.today()
    now = now.strftime("%m/%d/%Y")
    try:
        url_lenta = "https://lenta.ru"
        url_lenta_news = url_lenta + "/parts/news/"
        response = requests.get(url_lenta_news, headers=headers)
        root = html.fromstring(response.text)
        elements = root.xpath('//*/div[@class="item news"]')

        news_lst = []
        for el in elements:
            lst = {}
            a_source = el.xpath('.//div[1]/a/text()')
            a_source_link = el.xpath('.//div[1]/a/@href')
            news = el.xpath('.//div[2]/h3/a/text()')
            link = el.xpath('.//div[2]/h3/a/@href')
            data_news = el.xpath('.//div[1]/text()')

            try:
                lst['source'] = a_source[0]
            except:
                lst['source'] = a_source_link[0].replace("http://", "")

            lst['news'] = news[0].replace("\xa0", " ")
            lst['link'] = f"{url_lenta}{link[0]}"
            if len(data_news[0])<=5:
                lst['data_news'] = f"{now} {data_news[0]}"  #data_news[0]
            else:
                lst['data_news'] = data_news[0]
            lst['site'] = "lenta.ru"

            news_lst.append(lst)

        return news_lst
    except:
        print('Ошибка запроса к сайту lenta.ru')


def parse_news_yandex(params, headers):
    now = date.today()
    now=now.strftime("%m/%d/%Y")
    try:
        url_ya = "https://yandex.ru"
        url_ya_news = url_ya + "/news"
        response = requests.get(url_ya_news, params, headers=headers)
        root = html.fromstring(response.text)

        elements = root.xpath('//*/div[contains(@class,"mg-card__text-content")]')

        news_lst = []
        for el in elements:
            lst = {}
            link = el.xpath('.//div[1]/a/@href')
            news = el.xpath('.//div[1]/div[1]/text()')

            a_source = el.xpath('./..//*/span[contains(@class,"source__source")]/a/text()')
            if len(a_source) == 0:
                a_source = el.xpath('./../..//*/span[contains(@class,"source__source")]/a/text()')

            data_news = el.xpath('./..//*/span[contains(@class,"source__time")]/text()')
            if len(data_news) == 0:
                data_news = el.xpath('./../..//*/span[contains(@class,"source__time")]/text()')

            lst['source'] = ''.join(a_source)
            lst['news'] = ''.join(news)
            lst['link'] = ''.join(link)
            if len(data_news[0])<=5:
                lst['data_news'] = f"{now} {data_news[0]}"
            else:
                lst['data_news'] = ''.join(data_news)
            lst['site'] = "yandex.ru"
            news_lst.append(lst)
        return news_lst
    except:
        print('Ошибка запроса к ya.ru')

def parse_news_mail(params, headers):
    try:
        url_mail = "https://news.mail.ru/"
        response = requests.get(url_mail, params, headers=headers)
        root = html.fromstring(response.text)
        lst = []

        elements = root.xpath('//*/div[contains(@class,"js-modul")]')
        for el in elements:
            link = el.xpath('.//*/div[contains(@class,"daynews__item_big")]/a/@href')
            if len(link) != 0:
                break
        lst.append(''.join(link))

        for el in elements:
            link = el.xpath('.//*/tr/td[contains(@class,"daynews__items")]/div/a/@href')
            if len(link) != 0:
                break
        for el_list in link:
            lst.append(el_list)

        for el in elements:
            link = el.xpath('.//*/ul/li/a/@href')
            if len(link) != 0:
                break

        for el_list in link:
            lst.append(el_list)

        news_lst = []
        for el_lnk in lst:
            el_lst = {}
            response = requests.get(el_lnk, params, headers=headers)
            root_link = html.fromstring(response.text)
            news = root_link.xpath('//*/h1[contains(@class,"hdr__inner")]/text()')
            a_source = root_link.xpath('//*/h1[contains(@class,"hdr__inner")]/../../../..//*/a/span/text()')
            data_news = root_link.xpath('//*/h1[contains(@class,"hdr__inner")]/../../../..//*/span[@datetime]/@datetime')
            link = el_lnk
            site = "mail.ru"

            el_lst['source'] = ''.join(a_source)
            el_lst['news'] = ''.join(news)
            el_lst['link'] = link
            el_lst['data_news'] = ''.join(data_news)
            el_lst['site'] = site
            news_lst.append(el_lst)
        return news_lst
    except:
        print('Ошибка запроса к mail.ru')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
params = ""


news_lenta = parse_news_lenta(params, headers)
print(f"Новости с сайта lenta.ru: {len(news_lenta)}")
#pprint(news_lenta)

news_ya = parse_news_yandex(params, headers)
print(f"Новости с сайта ya.ru: {len(news_ya)}")
#pprint(news_ya)

news_mail = parse_news_mail(params, headers)
print(f"Новости с сайта ya.ru: {len(news_mail)}")
#pprint(news_mail)

all_news = news_lenta + news_ya + news_mail
pprint(all_news)
