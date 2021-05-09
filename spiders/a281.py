# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A281Spider(CrawlSpider):
    name = '281'
    allowed_domains = ['wl.cq.gov.cn']
    start_urls = ['http://wl.cq.gov.cn/zwgk/131/']

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/news/\d+-\d+/\d+_\d+\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/\d+$'), follow=True),
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

        contents = response.xpath('//div[@id="newscontent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
