# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A166Spider(CrawlSpider):
    name = '166'
    allowed_domains = ['yugan.gov.cn']
    start_urls = ['http://www.yugan.gov.cn/news-list-zhengwugongkai.html']

    rules = (
        Rule(LinkExtractor(allow=r'/news-list-[a-z]+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/xxgk-list-[a-z]+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/xxgk-list-[a-z]+\-\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/xxgk-show-\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/news-show-\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/news-list-[a-z]+-\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="show"]/div[2]/div[3]/span/span[3]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="show_title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
