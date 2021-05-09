# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A377Spider(CrawlSpider):
    name = '377'
    allowed_domains = ['kmdc.gov.cn']
    start_urls = ['http://kmdc.gov.cn/gggs/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="sideMenu"]//h3'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="sideMenu"]//ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="list_txtsbg"]/ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.shtml'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="time"]/span[2]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="timu"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="txtcen"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
