# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A587Spider(CrawlSpider):
    name = '587'
    allowed_domains = ['mfx.gov.cn']
    start_urls = [
        'http://www.mfx.gov.cn/zwgk/index.html',
        'http://www.mfx.gov.cn/xxdt/index.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/\d+/\d+/\d+/[a-z]+/\d+\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/\d+/\d+/\d+/zwgk/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[4]/div[3]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[4]/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/div[4]/div[4]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
