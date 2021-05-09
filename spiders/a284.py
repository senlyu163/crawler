# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A284Spider(CrawlSpider):
    name = '284'
    allowed_domains = ['cqfj.gov.cn']
    start_urls = ['http://www.cqfj.gov.cn/zwgk/169/']

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/news/\d+-\d+/\d+_\d+\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.shtml'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="newsdate"]').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="newstitle"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/table/tr/td[2]/div/table[1]/tr/td/table/tr/td/table[3]/tr/td').extract()
        item['contents'] = extract_CN_from_content(contents)

        year = date[:4]
        if int(year) >= 2015 and int(year) <= 2019:
            return item
