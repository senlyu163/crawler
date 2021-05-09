# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A186Spider(CrawlSpider):
    name = '186'
    allowed_domains = ['ningling.gov.cn']
    start_urls = ['http://www.ningling.gov.cn/xxgk/zfxxgk/']

    rules = (
        Rule(LinkExtractor(allow=r'/xxgk/[a-z]+$'), follow=True),
        Rule(LinkExtractor(allow=r'/xxgk/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="navjz"]/ul[1]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/xxgk/[a-z]+/index_\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="color_printsssss"]/div[1]/div/span[1]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="color_printsssss"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="zoom"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
