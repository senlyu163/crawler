# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A542Spider(CrawlSpider):
    name = '542'
    allowed_domains = ['xiahe.gov.cn']
    start_urls = ['http://www.xiahe.gov.cn/qtpagedata/infogklist433.html']

    rules = (
        Rule(LinkExtractor(allow=r'/qtpagedata/infogklist\d+_\d+/.html'), follow=True),
        Rule(LinkExtractor(allow=r'/qtpagedata/infogklist\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/qtpagedata/infogkdisp\d+\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/qtpagedata/infogklist\d+_\d+\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@id="articaldiv"]/div[2]').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@id="titlediv"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="articalcontent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
