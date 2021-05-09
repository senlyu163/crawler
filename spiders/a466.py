# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

# class A466Spider(CrawlSpider):
#     name = '466'
#     allowed_domains = ['yanchuan.gov.cn']
#     start_urls = ['http://www.yanchuan.gov.cn/list-1844.html']
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/list-\d+\.html'), follow=True),
#         Rule(LinkExtractor(allow=r'/thread-\d+-\d+\.html'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'list-\d+-\d+\.html'), follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#     def parse_item(self, response):
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('//*[@id="color_printsssss"]/div[3]/table/tr[1]/td[2]').extract_first()
#         date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('//*[@id="color_printsssss"]/div[3]/table/tr[3]/td/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@id="MyContent"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item
