# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A198Spider(CrawlSpider):
    name = '198'
    allowed_domains = ['xincai.gov.cn']
    start_urls = ['http://www.xincai.gov.cn/a/zhengfuxinxigongkai/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pen"]/ul[1]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list_\d+_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[4]/text()').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[2]/div[2]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="pen padNone"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
