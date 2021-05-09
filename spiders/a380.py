# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A380Spider(CrawlSpider):
    name = '380'
    allowed_domains = ['qjfy.gov.cn']
    start_urls = ['http://www.qjfy.gov.cn/html/zwgk/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="w_title"]/ul[1]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="list_more"]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="list_matter_ul"]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/zwgk/.*/\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="content_source"]/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="content_title"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
