# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies

    def process_item(self, item, spider):
        if spider.name == "sjru":
            item['salary_min'], item['salary_max'], item['salary_cur'] = self.process_salary_sj(item['salary_min'])

        if spider.name == "hhru":
            item['salary_min'], item['salary_max'], item['salary_cur'] = self.process_salary_hh(item['salary_min'])

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        txt = " ".join(salary)
        find_min = txt.find('vac_salary_from')
        findmax = txt.find('vac_salary_to')
        findCur = txt.find('vac_salary_cur')
        findCur_ = txt.find('vac_profarea')
        strmin = txt[find_min: findmax]
        min_s = strmin[(strmin.index(":") + 3):(strmin.index("\n") - 2)]
        strmax = txt[findmax: findCur]
        max_s = strmax[(strmax.index(":") + 3):(strmax.index("\n") - 2)]
        strcur = txt[findCur: findCur_]
        cur_s = strcur[(strcur.index(":") + 3):(strcur.index("\n") - 2)]

        if min_s == "":
            min_s = 0
        else:
            min_s = int(min_s)

        if max_s == "":
            max_s = 0
        else:
            max_s = int(max_s)

        return min_s, max_s, cur_s

    def process_salary_sj(self, salary):
        salary = " ".join(salary)
        salary = salary.replace(u'\xa0', u'')

        if '—' in salary:
            salary_min = salary.split('—')[0]
            salary_min = re.sub(r'[^0-9]', '', salary_min)
            salary_max = salary.split('—')[1]
            salary_max = re.sub(r'[^0-9]', '', salary_max)
            salary_min = int(salary_min)
            salary_max = int(salary_max)
        elif 'от' in salary:
            salary_min = salary[2:]
            salary_min = re.sub(r'[^0-9]', '', salary_min)
            salary_min = int(salary_min)
            salary_max = None
        elif 'договорённости' in salary:
            salary_min = None
            salary_max = None
        elif 'до' in salary:
            salary_min = None
            salary_max = salary[2:]
            salary_max = re.sub(r'[^0-9]', '', salary_max)
            salary_max = int(salary_max)
        else:
            salary_min = int(re.sub(r'[^0-9]', '', salary))
            salary_max = int(re.sub(r'[^0-9]', '', salary))

        if salary_min == None:
            salary_min = 0
        else:
            salary_min = int(salary_min)

        if salary_max == None:
            salary_max = 0
        else:
            salary_max = int(salary_max)

        if salary_min == 0 and salary_max == 0:
            cur = None
        else:
            cur = salary[len(salary) - 4:]

        return salary_min, salary_max, cur
