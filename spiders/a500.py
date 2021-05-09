# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A500Spider(CrawlSpider):
    name = '500'
    allowed_domains = ['yzx.lanzhou.gov.cn']
    start_urls = [
        'http://yzx.lanzhou.gov.cn/col/col9445/index.html',
        'http://yzx.lanzhou.gov.cn/col/col1802/index.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/col/col\d+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/art/.*/art_\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/col/col\d+/index\.html\?uid=\d+&pageNum=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="c"]/tr[2]/td/div/table/tr/td[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="c"]/tr[1]/td/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="zoom"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item