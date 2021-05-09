# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A505Spider(CrawlSpider):
    name = '505'
    allowed_domains = ['xxgk.gangu.gov.cn']
    start_urls = ['http://xxgk.gangu.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'/index\.php\?m=content&c=index&a=lists&catid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/index\.php\?m=content&c=index&a=show&catid=\d+&id=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index\.php\?m=content&c=index&a=lists&catid=\d+&page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/table/tr/td/table[5]/tr/td/table[2]/tr/td/span').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/table/tr/td/table[5]/tr/td/table[1]/tr/td/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/table/tr/td/table[5]/tr/td/table[5]/tr').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
