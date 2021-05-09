# -*- coding: utf-8 -*-
import scrapy
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A591ScrapySpider(scrapy.Spider):
    name = '591_scrapy'
    allowed_domains = ['xjqh.gov.cn']
    start_urls = []

    url_template = "http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex={}"
    for n in range(229):
        url = url_template.format(n + 1)
        start_urls.append(url)

    def parse(self, response):
        table_urls = response.xpath('//ul[@id="govinfolist"]//li').extract()

        # print(">>>>>>>>>>>>>>>>>>>>>>>>>  ", response.url)

        for tu in table_urls:
            yield scrapy.Request(url=tu, callback=self.extract_content)

    def extract_content(self, response):

        print(">>>>>>>>>>>>>>>>>>>>>>  ", response.url)

        # item = ScrapySpiderItem()
        # item['url'] = response.url
        #
        # date = response.xpath('//*[@id="container"]/div[3]/div/div/div[1]/table/tr[3]/td[4]/span').extract_first()
        # date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        # item['date'] = date
        #
        # title = response.xpath(
        #     '//*[@id="container"]/div[3]/div/div/div[1]/table/tr[1]/td[2]/span/text()').extract_first()
        # item['title'] = title
        #
        # contents = response.xpath('//div[@class="ewb-article"]').extract()
        # item['contents'] = extract_CN_from_content(contents)
        # return item
