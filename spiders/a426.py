# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A426Spider(CrawlSpider):
    name = '426'
    allowed_domains = ['xczw.gov.cn']
    start_urls = [
        'https://www.xczw.gov.cn/Category_354/Index.aspx',
        'https://www.xczw.gov.cn/Category_175/Index.aspx',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/Category_\d+/Index\.aspx'), follow=True),
        Rule(LinkExtractor(allow=r'/Item/\d+\.aspx'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'Index_\d+\.aspx'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="property"]/span[3]/text()').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//h2[@class="title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="conTxt"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
