# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A164Spider(CrawlSpider):
    name = '164'
    allowed_domains = ['srx.gov.cn']
    start_urls = [
        'http://www.srx.gov.cn/gk/bmxxgkml',
        'http://www.srx.gov.cn/publicity/shgysy/tpgj',
        'http://www.srx.gov.cn/gk',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/publicity/shgysy/[a-z]+$'), follow=True),
        Rule(LinkExtractor(allow=r'/publicity_[a-z]+/[a-z]+/[a-z]+/\d+$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/publicity/shgysy/[a-z]+_\d+$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="departmentType-1"]/div[2]/ul/div/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="row1"]/div[2]/div[1]/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="content"]/div/div/div[2]/div/div[2]/div'), follow=True),
        Rule(LinkExtractor(allow=r'/[a-z]+/[a-z]+$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/publicity/shgysy/[a-z]+__[a-z]+/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="content"]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="content"]/div/div/div[2]/div[2]/div[1]/div/h3/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="govDetail"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath(
                '//*[@id="content"]/div/div/div/div/div/div/div[1]/div[1]/span[2]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="content"]/div/div/div/div/div/div/div[1]/h3/center/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//*[@id="content"]/div/div/div/div/div/div/div[1]/div[2]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
