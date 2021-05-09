# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A79Spider(CrawlSpider):
    name = '79'
    allowed_domains = ['linxixian.gov.cn']
    start_urls = ['http://www.linxixian.gov.cn/zwgk/jzxxgkml/']

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/[a-z]+$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/[a-z]+/\d+-\d+-\d+-\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/\?pi=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/[a-z]+/\?pi=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="article_Top"]/div/div[1]/div[1]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="article_Top"]/div/div[1]/h1/span/font/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="articleContnet"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
