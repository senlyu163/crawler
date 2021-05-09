# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A419Spider(CrawlSpider):
    name = '419'
    allowed_domains = ['lx.hh.gov.cn']
    start_urls = [
        'http://www.lx.hh.gov.cn/xwzx/zwyw/',
        'http://www.lx.hh.gov.cn/xxgk/ggml/4523/4538/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="xw-main-left lf"]/ul//li'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[4]/div[2]/div[2]/div/div[1]/p[4]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[4]/div[2]/div[2]/div/div[1]/p[7]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//div[@class="xl-details-source"]/p/span').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//h1[@class="xl-details-title"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="TRS_Editor"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
