import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


# ----------------------------------------------------------- SuperJob -------------------------
class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    # start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=data']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Data&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']/a/@href").extract()

        next_page = response.xpath("//a[contains(@class,'dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_data = response.xpath("//h1/text()").extract_first()
        salary_data = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract()
        link_data = response.url
        site_data = "superjob"
        # .extract_first()
        yield JobparserItem(name = name_data, salary_min = salary_data, link = link_data, site = site_data)
