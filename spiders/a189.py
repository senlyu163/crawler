# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A189Spider(CrawlSpider):
    name = '189'
    allowed_domains = ['hnxx.gov.cn']
    start_urls = ['http://www.hnxx.gov.cn/xxgk/gkml/A0502index_1.htm']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="list_right"]/ul[1]//li/span[2]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/xxgk/gkml/A0502index_\d+\.htm'), follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[2]/div[1]/div/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="detail_body"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
