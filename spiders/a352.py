# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A352Spider(CrawlSpider):
    name = '352'
    allowed_domains = ['gzdafang.gov.cn']
    start_urls = [
        'http://www.gzdafang.gov.cn/zwgk/dfxzfxxgkml/fgwj/zfwj/',
        'http://www.gzdafang.gov.cn/zwgk/zdlygk/czzj/xbjczyjsjsgjf/index.html',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="tree_box pd10"]/ul//li/ul//li/span'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="angnq"]/dl/dt//div/ul//li'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//div[@class="xxly"]').extract_first()
            date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//div[@class="contTextBox"]/h3/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="detail_main_content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//div[@class="detail_main_xx"]').extract_first()
            date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//div[@class="detail_main_title"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="detail_main_content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
