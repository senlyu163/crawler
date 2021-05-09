# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A81Spider(CrawlSpider):
    name = '81'
    allowed_domains = ['klq.gov.cn']
    start_urls = ['http://www.klq.gov.cn/channels/298.html']

    rules = (
        Rule(LinkExtractor(allow=r'/channels/\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/contents/\d+/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/channels/\d+_\d+\.html'), follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[5]/div/div[3]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[5]/div/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="nr"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
