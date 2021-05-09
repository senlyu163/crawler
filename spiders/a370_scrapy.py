# -*- coding: utf-8 -*-
import scrapy

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
import time
import requests


class A370ScrapySpider(scrapy.Spider):
    name = '370_scrapy'
    allowed_domains = ['qdndz.gov.cn']
    start_urls = ['http://www.qdndz.gov.cn/xxgk/xxgkml/jcgk/zcwj/xzfwj/index.html']

    def parse(self, response):
        navi_list = response.xpath('//div[@class="tab-pal"]//ul//span/a/@href').extract()
        for nl in navi_list:
            if 'xxgk' in nl:
                yield scrapy.Request(url=nl, callback=self.get_navi_url)
            else:
                continue

    def get_navi_url(self, response):
        url_lib = []
        if "index" in response.url:
            wanna_url = response.url[:-10]
            url_lib.append(wanna_url)
        else:
            url_lib.append(response.url)

        # add FuPinKaiFa item
        url_lib.append('http://www.qdndz.gov.cn/xxgk/xxgkml/zdlygk/fpgz')

        for u_lib in url_lib:
            yield scrapy.Request(url=u_lib, callback=self.extract_table_url)
            for i in range(1000):
                # time.sleep(1)
                complete_url = u_lib + "list_{}.html".format(i + 1)
                if requests.get(url=complete_url).status_code == int('200'):
                    yield scrapy.Request(url=complete_url, callback=self.extract_table_url)
                else:
                    break

    def extract_table_url(self, response):
        table_url = response.xpath('//*[@id="data"]//tr/td[1]/h1/a/@href').extract()
        for tu in table_url:
            # time.sleep(1)
            yield scrapy.Request(url=tu, callback=self.extract_context)

    def extract_context(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="title"]/div[1]').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="title"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content2"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item