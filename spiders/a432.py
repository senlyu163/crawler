# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A432Spider(CrawlSpider):
    name = '432'
    allowed_domains = ['ynml.gov.cn']
    start_urls = ['https://www.ynml.gov.cn/107.news.list.dhtml']

    rules = (
        Rule(LinkExtractor(allow=r'/\d+\.news\.list\.dhtml'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+\.news\.detail\.dhtml\?news_id=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/\d+\.news\.list\.dhtml\?page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="news-detail"]/p[2]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="news-detail"]/p[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="news"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        year = date[:4]
        if int(year) >= 2015 and int(year) <= 2019:
            return item
