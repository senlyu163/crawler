# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A124Spider(CrawlSpider):
    name = '124'
    allowed_domains = ['hljfy.gov.cn']
    start_urls = ['http://www.hljfy.gov.cn/zwgk/']

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="cha_text divb"]/ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.htm'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="main"]/div[2]/div[2]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="main"]/div[2]/div[1]/strong/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="logPanel"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item