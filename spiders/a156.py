# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A156Spider(CrawlSpider):
    name = '156'
    allowed_domains = ['xunwu.gov.cn']
    start_urls = ['http://www.xunwu.gov.cn/zwgk/']

    rules = (
        Rule(LinkExtractor(allow=r'/zdlygk/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="menuList"]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="newsList"]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="list_m"]/table[1]//tr/td[2]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.htm'), follow=True),
        # Rule(LinkExtractor(allow=r'index_\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[3]/div[2]/div[1]/table/tr[2]/td[1]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[3]/div[2]/h2/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/div[3]/div[2]/div[2]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="content"]/article/div[1]/div[1]/span[2]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="content"]/article/div[1]/h2/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="TRS_Editor"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
