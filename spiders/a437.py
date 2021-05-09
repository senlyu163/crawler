# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A437Spider(CrawlSpider):
    name = '437'
    allowed_domains = ['ypx.gov.cn']
    start_urls = [
        'http://www.ypx.gov.cn/ypxrmzf/c102105/common_list.shtml',
        'http://www.ypx.gov.cn/ypxrmzf/c102095/common_list.shtml',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/ypxrmzf/c\d+/common_list\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/ypxrmzf/c\d+/\d+/.*\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'common_list_\d+\.shtml'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="detail"]/div[1]').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="detail"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="NewsContent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
