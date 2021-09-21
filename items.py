# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import MapCompose, TakeFirst
import scrapy


def get_price(value):
    try:
        value = value.replace(' ', '')
        return int(value)
    except:
        return value

class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
    params = scrapy.Field()
    article = scrapy.Field(output_processor=TakeFirst())
    chapter = scrapy.Field(output_processor=TakeFirst())
