# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A62Spider(CrawlSpider):
    name = '62'
    allowed_domains = ['bdx.sxxz.gov.cn']
    start_urls = ['http://bdx.sxxz.gov.cn/bdxzw/zwgk/wj/gwywj/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="left-nav"]/li/ul//li'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div/div/div[2]/p').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div/div/div[2]/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="article-con"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
