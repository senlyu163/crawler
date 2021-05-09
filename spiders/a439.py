# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A439Spider(CrawlSpider):
    name = '439'
    allowed_domains = ['ey.yn.gov.cn']
    start_urls = ['http://www.ey.yn.gov.cn/eygov/1587518868648099840/']

    rules = (
        Rule(LinkExtractor(allow=r'/eygov/\d+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/eygov/\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/eygov/\d+/\d+/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\d+_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/table[3]/tr[5]/td/table[1]/tr[2]/td/table/tr[2]/td').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/table[3]/tr[5]/td/table[1]/tr[2]/td/table/tr[1]/td/strong/font/text()').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/table[3]/tr[5]/td/table[1]/tr[2]/td/table/tr[6]/td').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
