import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


# ----------------------------------------------------------- HH -------------------------
class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=data']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_data = response.xpath("//h1/text()").extract_first()
        #salary_data = response.xpath("//p[@class='vacancy-salary']/span/text()").extract_first()
        # "//script[@data-name='HH/GoogleDfpService']/@data-params"
        salary_data = response.xpath("//script[@data-name='HH/GoogleDfpService']/@data-params").extract()
        link_data = response.url
        site_data = "superjob"
        yield JobparserItem(name=name_data, salary_min=salary_data, link=link_data, site=site_data)

