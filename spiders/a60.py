# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A60Spider(CrawlSpider):
    name = '60'
    allowed_domains = ['klx.sxxz.gov.cn']
    start_urls = ['http://klx.sxxz.gov.cn/klxzw/zwgk/zcjd/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li[1]/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li[1]/ul/li[4]/dl//dd'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li[1]/ul/li[6]/dl//dd'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li[1]/ul/li[10]/dl//dd'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li[1]/ul/li[11]/dl//dd'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[2]/div[1]/div/div[1]/p').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[2]/div[1]/div/div[1]/h2/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="article-con"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[2]/div/div/div[1]/table/tr[5]/td[2]/span[3]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[2]/div/div/div[1]/table/tr[4]/td/span[3]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="article-con"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
