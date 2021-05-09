# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A288Spider(CrawlSpider):
    name = '288'
    allowed_domains = ['cqxs.gov.cn']
    start_urls = [
        'http://www.cqxs.gov.cn/zfxx/default_0_2_0.shtml?key=&w=quanbu&y=0',
        'http://www.cqxs.gov.cn/zfxx/23/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'web_show_\d+\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zfxx/default_0_2_\d+\.shtml\?Key=&w=quanbu&y=0&PublisherID=Identifier=sdate=edate=GWZ=NH=QH=SubjectCategoryName=ThemeCategoryName=SubjectTermName=&'), follow=True),

        Rule(LinkExtractor(allow=r'/zfxx/\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/zfxx/news/\d+-\d+/\d+_\d+\.shtml'), callback='parse_item_2', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.shtml'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="printbody"]/table/tr[2]/td[4]').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="printbody"]/table/tr[3]/td[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="printbody"]/table/tr[5]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def parse_item_2(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="newsdate"]').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="newstitle"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//span[@id="newscontent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
