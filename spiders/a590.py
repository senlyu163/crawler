# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A590Spider(CrawlSpider):
    name = '590'
    allowed_domains = ['xjtl.gov.cn']
    start_urls = ['http://www.xjtl.gov.cn/db3ea38e29195547944f532980d99fb1.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="info_detial"]/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="list_con"]/ul//li/h4'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="page"]'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[4]/ul/li[2]/div[1]/ul/p').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[4]/ul/li[2]/div[1]/ul/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="detial_news"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
