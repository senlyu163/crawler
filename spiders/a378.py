# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A378Spider(CrawlSpider):
    name = '378'
    allowed_domains = ['lq.km.gov.cn']
    start_urls = [
        'http://lq.km.gov.cn/zfxxgkml/ysqgk/',
        'http://lq.km.gov.cn/zfxxgkml/zzjg/xxgkgzjgxx/',
        'http://lq.km.gov.cn/zfxxgkml/zfwj/',
        'http://lq.km.gov.cn/zfxxgkml/zfgbgb/',
        'http://lq.km.gov.cn/zfxxgkml/zcjd/',
        'http://lq.km.gov.cn/zfxxgkml/zfxxgkndbg/',
        'http://lq.km.gov.cn/zfxxgkml/zfgzbg/',
        'http://lq.km.gov.cn/zfxxgkml/zdgzxx/',
        'http://lq.km.gov.cn/zfxxgkml/czzjxx/',
        'http://lq.km.gov.cn/zfxxgkml/zfcg/',
        'http://lq.km.gov.cn/zfxxgkml/rsxx/',
        'http://lq.km.gov.cn/zfxxgkml/zdxmxx/',
        'http://lq.km.gov.cn/zfxxgkml/jhgh/',
        'http://lq.km.gov.cn/zfxxgkml/tjxx/',
        'http://lq.km.gov.cn/zfxxgkml/yjgl/',
        'http://lq.km.gov.cn/zfxxgkml/rdhy/',
        'http://lq.km.gov.cn/zfxxgkml/zdlyxxgk/',
        'http://lq.km.gov.cn/zfxxgkml/jytabljg/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/c/\d+-\d+-\d+/\d+\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.shtml'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//ul[@class="list"]/li[4]/span').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//li[@class="article-name"]/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="L2"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
