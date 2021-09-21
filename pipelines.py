# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes


class LeruaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlen

    def process_item(self, item, spider):
        collection = self.mongo_base['load']
        # код если хотим хранить запросы в разных коллекциях в базе mongodb
        # collection = self.mongo_base[item['chapter']]
        # ниже храним только в одной коллекциии
        if collection.count_documents({'article': item['article']}) == 0:
            collection.insert_one(item)
        return item


class LeruaPhotosPipeline(ImagesPipeline):
    # pip install pillow - не забыть установить
    def get_media_requests(self, item, info):
        print()
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print()
        if results:
            item["photos"] = [itm[1] for itm in results if itm[0]]
        return item

    # организаия хранения файлов в разных директориях
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        full = item['article']  # "full"
        return f'{full}/{full}_{image_guid}.jpg'
