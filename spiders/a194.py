# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A194Spider(CrawlSpider):
    name = '194'
    allowed_domains = ['huaiyang.gov.cn']
    start_urls = [
        'http://www.huaiyang.gov.cn/list-1179.html',
        'http://www.huaiyang.gov.cn/list-1180.html',
        'http://www.huaiyang.gov.cn/list-1177.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/thread-\d+-\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list-\d+-\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="article"]/p[1]/span[1]/text()').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="article"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="MyContent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
