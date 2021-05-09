# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A66Spider(CrawlSpider):
    name = '66'
    allowed_domains = ['sxxx.gov.cn']
    start_urls = ['http://www.sxxx.gov.cn/channels/4861.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div[1]/div'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div[2]/div[1]/div[2]/div/div//ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div[2]/div[2]/a[8]'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
