# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A191Spider(CrawlSpider):
    name = '191'
    allowed_domains = ['gsxzf.gov.cn']
    start_urls = ['http://www.gsxzf.gov.cn/gsxrmzf/zwgk/A0102index_1.htm']

    rules = (
        Rule(LinkExtractor(allow=r'/gsxrmzf/zwgk/[a-z]+/A\d+index_\d+\.htm$'), follow=True),
        Rule(LinkExtractor(allow=r'/gsxrmzf/zwgk/[a-z]+/[a-z]+/webinfo/\d+/\d+/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/gsxrmzf/zwgk/[a-z]+/[a-z]+/A\d+index_\d+\.htm'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="l_zwnr_info"]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="l_zwnr_title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="BodyLabel"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
