# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A260Spider(CrawlSpider):
    name = '260'
    allowed_domains = ['gxfc.gov.cn']
    start_urls = [
        'https://www.gxfc.gov.cn/zwgk'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="zf-news"]/h2'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+\.do'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/page/\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+-zwgk$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/zdlyxxgk/[a-z]+$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="pubDate"]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content clearfix"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
