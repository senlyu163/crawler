# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A287Spider(CrawlSpider):
    name = '287'
    allowed_domains = ['cqszx.gov.cn']
    start_urls = ['http://www.cqszx.gov.cn/zfxx/List.asp?dwCode=00913403X&SubjectCategoryCode=&ThemeCategoryCode=&TitleKeyWords=']

    rules = (
        Rule(LinkExtractor(allow=r'/zfxx/show/\?id=\d+$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'List\.asp\?dwCode=00913403X&SubjectCategoryCode=&ThemeCategoryCode=&TitleKeyWords=&flag=&smod=&KeyWords=&sYear=0&page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="contentx1"]/table/tbody/tr[2]/td[2]').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="text"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="showcontent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
