# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A219Spider(CrawlSpider):
    name = '219'
    allowed_domains = ['xe.gov.cn']
    start_urls = [
        'http://www.xe.gov.cn/xuanen/xxgk/',
        'http://www.xe.gov.cn/xuanen/xxgk/gkml/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//dd[@class="clear ofh p10"]/ul[1]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="lists"]/ul[1]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/xuanen/[a-z]+/[a-z]+/\d+\.shtml'), follow=True),

        Rule(LinkExtractor(restrict_xpaths='//*[@id="loop"]/div[2]/dl[2]/dd/ul[1]//li'), follow=True),
        Rule(LinkExtractor(allow=r'/xuanen/[a-z]+/[a-z]+/[a-z]+/\d+\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'xe\.gov\.cn/\d+/\d+/\d+\.shtml'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="info-date"]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="article"]/div[2]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
