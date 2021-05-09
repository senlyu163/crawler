# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

'''
class ScrapySpiderPipeline(object):
    # pass
    # 自定义json文件导出
    def __init__(self):
        self.name = None
        self.file = None
    #     filename = 'lingshou' # change filename according to the name of website
    #     self.name = filename
    #     self.file = codecs.open('./json_files/{}.json'.format(self.name), 'w', encoding="utf-8")
    #
    def process_item(self, item, spider):
        self.name = spider.name
        # self.file = codecs.open('./json_files/{}.json'.format(self.name), 'a', encoding="utf-8")
        self.file = codecs.open('/home/sen/Workspace/handle_data/lab_scrapy/spider_crawl_start_55/scrapy_spider/scrapy_spider/json_files/{}.json'.format(self.name), 'a', encoding="utf-8")
        lines = json.dumps(dict(item), ensure_ascii=False) + "," + "\n"
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.close()
        self.convert_mult_objects_to_list()

    def convert_mult_objects_to_list(self):
        import os
        with open('/home/sen/Workspace/handle_data/lab_scrapy/spider_crawl_start_55/scrapy_spider/scrapy_spider/json_files/{}.json'.format(self.name), "rb+") as json_file:
            json_file.seek(-2, os.SEEK_END)
            json_file.truncate()
        with open('/home/sen/Workspace/handle_data/lab_scrapy/spider_crawl_start_55/scrapy_spider/scrapy_spider/json_files/{}.json'.format(self.name), "a", encoding="utf-8") as json_file:
            json_file.write("]")
        with open('/home/sen/Workspace/handle_data/lab_scrapy/spider_crawl_start_55/scrapy_spider/scrapy_spider/json_files/{}.json'.format(self.name), "r+", encoding="utf-8") as f:
            content = f.read()
            f.seek(0)
            f.write('[' + content)


    #
    # def __init__(self):
    #     self.file = codecs.open('xingtang.json', 'w', encoding="utf-8")
    #
    # def process_item(self, item, spider):
    #     lines = json.dumps(dict(item), ensure_ascii=False) + "," + "\n"
    #     self.file.write(lines)
    #     return item
    #
    # def close_spider(self, spider):
    #     self.file.close()
    #     self.convert_mult_objects_to_list()
    #
    # def convert_mult_objects_to_list(self):
    #     import os
    #     with open('xingtang.json', "rb+") as json_file:
    #         json_file.seek(-2, os.SEEK_END)
    #         json_file.truncate()
    #     with open('xingtang.json', "a") as json_file:
    #         json_file.write("]")
    #     with open('xingtang.json', "r+") as f:
    #         content = f.read()
    #         f.seek(0)
    #         f.write('[' + content)

'''


import json

from itemadapter import ItemAdapter

class JsonWriterPipeline:

    def open_spider(self, spider):
        # self.file = open('items.jl', 'w')
        self.name = spider.name
        # self.file = codecs.open('./json_files/{}.json'.format(self.name), 'a', encoding="utf-8")
        self.file = codecs.open('/home/sen/Workspace/handle_data/lab_scrapy/spider_crawl_start_55/scrapy_spider/scrapy_spider/json_files/{}.json'.format(self.name), 'a', encoding="utf-8")
        # lines = json.dumps(dict(item), ensure_ascii=False) + "," + "\n"
        # self.file.write(lines)
        # return item

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "," + "\n"
        self.file.write(line)
        return item
