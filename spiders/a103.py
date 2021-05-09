# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A103Spider(CrawlSpider):
    name = '103'
    allowed_domains = ['sntyq.gov.cn']
    start_urls = ['http://www.sntyq.gov.cn/zwgk/tzgg/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="cont_bd"]/ul[1]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="nav_bd"]'), follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if response.url == "http://sousuo.gov.cn/s.htm?q=国务院文件&t=paper" or response.url == "http://sousuo.gov.cn/s.htm?t=govall&q=%E5%9B%BD%E5%8A%9E%E5%8F%91%E6%96%87%E4%BB%B6":
            pass
        else:
            try:
                item = ScrapySpiderItem()
                item['url'] = response.url

                date = response.xpath('//div[@class="cont_desc"]/text()').extract_first()
                date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
                item['date'] = date

                title = response.xpath('/html/body/div[2]/div/div[3]/h3/text()').extract_first()
                item['title'] = title

                contents = response.xpath('//div[@class="TRS_Editor"]').extract()
                item['contents'] = extract_CN_from_content(contents)
                return item
            except:
                print("have format error.")
