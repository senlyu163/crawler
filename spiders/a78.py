# -*- coding: utf-8 -*-
import scrapy

import requests
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A78Spider(scrapy.Spider):
    name = '78'
    allowed_domains = ['blyq.gov.cn']
    start_urls = ['http://www.blyq.gov.cn/zwxxgk/list-320/1.html']

    def parse(self, response):
        page_num = 300
        for i in range(page_num):
            next_url = 'http://www.blyq.gov.cn/zwxxgk/list-320/{}.html'.format(i+1)
            if requests.get(url=next_url).status_code == int("200"):
                yield scrapy.Request(url=next_url, callback=self.extract_table)
            else:
                break

    def extract_table(self, response):
        table_url = response.xpath('//div[@class="listy"]/ul[1]//li//a/@href').extract()
        for tu in table_url:
            complete_url = response.urljoin(tu)
            yield scrapy.Request(url=complete_url, callback=self.extract_context)

    def extract_context(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="listxx"]/h4[1]/span[2]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="listxx"]/h3[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="listxx"]/ul[1]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
