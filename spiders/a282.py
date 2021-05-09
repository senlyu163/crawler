# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A282Spider(CrawlSpider):
    name = '282'
    allowed_domains = ['kx.cq.gov.cn']
    start_urls = ['http://kx.cq.gov.cn/html/page/402880ec6eb177ab016eb177ab80000d.html']

    rules = (
        Rule(LinkExtractor(allow=r'/html/page/.*\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/text/.*\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/page/.*_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="text"]/h3').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="text"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="showcontent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item