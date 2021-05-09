# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A414Spider(CrawlSpider):
    name = '414'
    allowed_domains = ['yaoan.gov.cn']
    start_urls = ['http://www.yaoan.gov.cn/list20.aspx']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="clearfix ov-h zwlistbox"]/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="newzdtit"]/ul//li'), follow=True),
        Rule(LinkExtractor(allow=r'Pages_\d+_\d+\.aspx'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//ul[@id="fw"]/li[3]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//div[@class="read-title"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="readnr con"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//div[@class="from"]/span[3]').extract_first()
            date = re.search(r"(\d{4}/\d{1,2}/\d{1,2})", date).groups()[0]
            date = date.replace("/", "-")
            item['date'] = date

            title = response.xpath('//div[@class="read-title"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="readnr con"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
