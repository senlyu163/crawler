# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A193Spider(CrawlSpider):
    name = '193'
    allowed_domains = ['shenqiu.gov.cn']
    start_urls = [
        'http://www.shenqiu.gov.cn/zk_xxgk/news.asp?speid=30',
        'http://www.shenqiu.gov.cn/news.asp?msg=00239',
        'http://www.shenqiu.gov.cn/news.asp?msg=0203',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'news\.asp\?speid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'newslast\.asp\?id=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?page=\d+&speid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'news_xx\.asp\?msg=\d+'), callback='parse_item2', follow=True),
        Rule(LinkExtractor(allow=r'news\.asp\?page=\d+&msg=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div/table[4]/tr/td[2]/table/tr[2]/td/table[2]/tr/td').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div/table[4]/tr/td[2]/table/tr[2]/td/table[1]/tr/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/div/table[4]/tr/td[2]/table/tr[2]/td/table[3]/tr/td').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def parse_item2(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="table1"]/tr[2]/td/font/text()[1]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="table1"]/tr[1]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="table1"]/tr[3]/td').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
