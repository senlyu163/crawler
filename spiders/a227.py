# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A227Spider(CrawlSpider):
    name = '227'
    allowed_domains = ['pingjiang.gov.cn']
    start_urls = [
        'http://www.pingjiang.gov.cn/35048/35049/35052/default.htm',
        'http://www.pingjiang.gov.cn/35048/35049/35052/default.htm',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="lists"]//div/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="list_menu"]//li'), follow=True),
        Rule(LinkExtractor(allow=r'default_\d+\.htm'), follow=True),  # next page
        Rule(LinkExtractor(allow=r'\d+/\d+/content_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.htm'), follow=True),  # next page
        Rule(LinkExtractor(allow=r'content_\d+\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[5]/table/tbody/tr[2]/td[4]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[5]/h2/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@id="content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[5]/div[1]/table/tr/td[2]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[5]/h2/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@id="content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
