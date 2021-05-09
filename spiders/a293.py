# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A293Spider(CrawlSpider):
    name = '293'
    allowed_domains = ['gyct.gov.cn']
    start_urls = ['http://www.gyct.gov.cn/xxgk/zdxx/xzql.htm']

    rules = (
        Rule(LinkExtractor(allow=r'/xxgk/.*/[a-z]+\.htm$'), follow=True),
        Rule(LinkExtractor(allow=r'/info/\d+/\d+\.htm$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'[a-z]+/\d+\.htm$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div/div[2]/form/table/tr[2]/td/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/div/div[2]/form/table/tr[1]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="vsb_content_2"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
