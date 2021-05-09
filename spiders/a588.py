# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A588Spider(CrawlSpider):
    name = '588'
    allowed_domains = ['xjcbcr.gov.cn']
    start_urls = ['http://www.xjcbcr.gov.cn/open/copy_1_xxgk-seach.jsp?ainfolist2079t=203&ainfolist2079p=2&ainfolist2079c=20&urltype=egovinfo.EgovSearchList&wbtreeid=1005&stype=simple&keysimplesearchword=&searchtype=&searchtime=']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="ainfolist2079"]/div[1]/table//tr/td[1]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?ainfolist\d+t=\d+&ainfolist\d+p=\d+&ainfolist\d+c=\d+&urltype=egovinfo\.EgovSearchList&wbtreeid=\d+&stype=simple&keysimplesearchword=&searchtype=&searchtime='), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[7]/div/div[3]/table/tr[1]/td/table/tr[2]/td/table/tr[1]/td[6]').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[7]/div/div[3]/table/tr[1]/td/table/tr[1]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="egovinfocontenttable"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
