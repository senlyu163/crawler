# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A405Spider(CrawlSpider):
    name = '405'
    allowed_domains = ['ynlx.gov.cn']
    start_urls = ['http://www.ynlx.gov.cn/lxqrmzf/lxqrmzf/xxgk76/zfwj68/qzfwj/index.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="left_daohang"]/div[1]/ul[1]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="left_daohang"]/div[1]/ul[1]//ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="cs_list"]//li/span[1]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="xilan_tab"]/tbody/tr[5]/td').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//h1[@id="jiuctit"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="cont_len"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
