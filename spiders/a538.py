# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A538Spider(CrawlSpider):
    name = '538'
    allowed_domains = ['hezuo.gov.cn']
    start_urls = ['http://www.hezuo.gov.cn/zwgk/']

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/.*/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/.*/index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//td[@class="info_text"]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="contentmain"]/table/tr/td[1]/table[2]/tr/td/table[1]/tr[1]/td/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//td[@id="text"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
