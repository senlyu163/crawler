# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A453Spider(CrawlSpider):
    name = '453'
    allowed_domains = ['longxian.gov.cn']
    start_urls = ['http://www.longxian.gov.cn/zwgk1.htm']

    rules = (
        Rule(LinkExtractor(allow=r'xxgk/.*urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/info/\d+/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?.*&urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//span[@class="timestyle1932"]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//td[@class="titlestyle1932"]/text()').extract_first()
            title = extract_CN_from_content(title)
            item['title'] = title

            contents = response.xpath('//div[@id="vsb_content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            try:
                item = ScrapySpiderItem()
                item['url'] = response.url

                date = response.xpath('//span[@class="timestyle1795"]/text()').extract_first()
                date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
                item['date'] = date

                title = response.xpath('//td[@class="titlestyle1795"]/text()').extract_first()
                title = extract_CN_from_content(title)
                item['title'] = title

                contents = response.xpath('//div[@id="vsb_content"]').extract()
                item['contents'] = extract_CN_from_content(contents)
                return item
            except:
                item = ScrapySpiderItem()
                item['url'] = response.url

                date = response.xpath('//span[@class="timestyle2064"]/text()').extract_first()
                date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
                item['date'] = date

                title = response.xpath('//td[@class="titlestyle2064"]/text()').extract_first()
                title = extract_CN_from_content(title)
                item['title'] = title

                contents = response.xpath('//div[@id="vsb_content"]').extract()
                item['contents'] = extract_CN_from_content(contents)
                return item
