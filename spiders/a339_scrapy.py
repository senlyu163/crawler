# -*- coding: utf-8 -*-
import scrapy

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
import requests
from scrapy_splash import SplashRequest
import time

class A339ScrapySpider(scrapy.Spider):
    name = '339_scrapy'
    allowed_domains = ['shiqian.gov.cn']
    start_urls = ['http://www.shiqian.gov.cn/zwgk/xxgkml/list.html']

    nxt_url_pattern = 'http://www.shiqian.gov.cn/zwgk/xxgkml/list_{}.html'
    for n in range(434):
        url = nxt_url_pattern.format(n+1)
        start_urls.append(url)

    def parse(self, response):
        yield SplashRequest(url=response.url, callback=self.extract_table_url, args={"wait": 1})
        for i in range(1000):
            time.sleep(1)
            nxt_url = self.nxt_url_pattern.format(i+1)
            if requests.get(url=nxt_url).status_code == int('200'):
                yield SplashRequest(url=nxt_url, callback=self.extract_table_url, args={"wait": 1})
            else:
                break

    def extract_table_url(self, response):
        url_list = response.xpath('//*[@id="data"]//tr/td[1]/h1/a/@href').extract()
        for ul in url_list:
            yield SplashRequest(url=ul, callback=self.extract_context, args={"wait": 1})

    def extract_context(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[4]/span').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[7]/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content2"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item