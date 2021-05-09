# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A433Spider(CrawlSpider):
    name = '433'
    allowed_domains = ['yangbi.gov.cn']
    start_urls = ['http://www.yangbi.gov.cn/ybyz/c102095/common_list.shtml']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="cont_left"]/ul[1]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="con_right"]/ul[1]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'common_list_\d+\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/ybyz/c\d+/common_list\.shtml'), follow=True),
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
