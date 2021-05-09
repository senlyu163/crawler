# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A118Spider(CrawlSpider):
    name = '118'
    allowed_domains = ['suibin.gov.cn']
    start_urls = ['https://www.suibin.gov.cn/zwgk/']

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="nr2"]/ul//li/div[1]/span'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="tm3"]/span[1]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="tm2"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="nr5"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
