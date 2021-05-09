# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A464Spider(CrawlSpider):
    name = '464'
    allowed_domains = ['fuping.gov.cn']
    start_urls = ['http://www.fuping.gov.cn/Home/Information/path/id/5.html']

    rules = (
        Rule(LinkExtractor(allow=r'/Home/Information/path/id/\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/Home/Information/detail/id/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/Home/Information/path/id/\d+/p/\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="info"]/span[2]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item