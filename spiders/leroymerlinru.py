# Урок 6. Scrapy. Парсинг фото и файлов
# Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
# ● название;
# ● все фото;
# ● параметры товара в объявлении;
# ● ссылка;
# ● цена.
#
# Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.
# Дополнительно:
# 2)Написать универсальный обработчик характеристик товаров, который будет формировать данные вне зависимости от их типа и количества.
#
# 3)Реализовать хранение скачиваемых файлов в отдельных папках, каждая из которых должна соответствовать собираемому товару

import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader
from lxml import html
from pprint import pprint



class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    # "https://leroymerlin.ru/search/?q=обои"
    # start_urls = ['http://leroymerlin.ru/']

    def __init__(self, search):
        super().__init__()
        self.search = search
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//div[contains(@class,'phytpj4_plp')]/a/@href")
        # обработка перехода на другую страничку
        # закомментировал данный код ввиду блокировки от сайта "Ignoring response <403...."
        #
        # next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

        # обход по ссылкам
        for link in ads_links:
            #link = ads_links[1] #для проверки работы на одном экземпляре
            yield response.follow(link, callback=self.ads_parse)

    def ads_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('article', "//span[@slot='article']/@content")
        root = html.fromstring(response.text)
        # загрузка в словарь наименование и измерение характеристик
        dictkeys = root.xpath("//dt[@class='def-list__term']/text()")
        dictname = root.xpath("//dd[@class='def-list__definition']/text()")
        dictname = [j.strip() for j in dictname]
        dictparamsh = dict(zip(dictkeys, dictname))
        loader.add_value('params', dictparamsh)
        loader.add_value('chapter', self.search)
        # loader.add_xpath('params_name', "//dt[@class='def-list__term']/text()")
        # loader.add_xpath('params_term', "//dd[@class='def-list__definition']/text()")

        loader.add_xpath('price', "//uc-pdp-price-view[@class='primary-price']/span[contains(@slot,'price')]/text()")
        # фото 1200 на 1200 на этих настройках сервер Леруа меня заблокировал
        # loader.add_xpath('photos', "//picture[@slot='pictures']/img[@itemprop='image']/@src")
        # перешел на более мелкие
        loader.add_xpath('photos',
                         "//uc-pdp-media-carousel[@slot='media-content']/img[@slot='thumbs']/@src")  # фото 82 на 82

        yield loader.load_item()
