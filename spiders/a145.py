# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A145Spider(CrawlSpider):
    name = '145'
    allowed_domains = ['lxxxgk.bozhou.gov.cn']
    start_urls = ['http://lxxxgk.bozhou.gov.cn/opennessSearch/?keywords=']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="z-listcc"]//li/p[3]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/opennessSearch/\?keywords=&page=\d+'), follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="container"]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[4]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="container"]/div[2]/div[2]/div[1]/table/tbody/tr[5]/td[4]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="news-contnet"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        year = date[:4]
        if int(year) >= 2015 and int(year) <= 2019:
            return item
