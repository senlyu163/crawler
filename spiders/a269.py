# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A269Spider(CrawlSpider):
    name = '269'
    allowed_domains = ['jinxiu.gov.cn']
    start_urls = ['http://www.jinxiu.gov.cn/xxgk.shtml']

    rules = (
        Rule(LinkExtractor(allow=r'/[a-z]+/[a-z]+/index\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'[a-z]+/\d+-\d+\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/index-\d+\.shtml'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="more-chlid-title"]'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[2]/div[1]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="article-con"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
