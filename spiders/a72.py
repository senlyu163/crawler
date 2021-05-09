# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A72Spider(CrawlSpider):
    name = '72'
    allowed_domains = ['lanxian.gov.cn']
    start_urls = ['http://www.lanxian.gov.cn/infopub/gzbg/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='/html/body/div/div[4]/div[2]//div'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="doc_info"]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="doc_title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="TRS_Editor"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
