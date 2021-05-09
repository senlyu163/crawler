# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A150Spider(CrawlSpider):
    name = '150'
    allowed_domains = ['shangyou.gov.cn']
    start_urls = ['http://www.shangyou.gov.cn/zw/xmwj/']

    rules = (
        Rule(LinkExtractor(allow=r'/zw/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="news-list-area"]//li/h1'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/table[2]/tr/td/table[2]/tr/td/table[1]/tr[2]/td/table/tr[2]/td[1]/span[2]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/table[2]/tr/td/table[2]/tr/td/table[1]/tr[1]/td/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/table[2]/tr/td/table[2]/tr/td/table[2]/tr/td').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[7]/div[2]/div[2]/span[1]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[7]/div[2]/div[1]/h1/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
