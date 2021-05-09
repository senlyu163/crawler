# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re

class A33Spider(CrawlSpider):
    name = '33'
    allowed_domains = ['haixing.gov.cn']
    start_urls = ['http://www.haixing.gov.cn/zwgk.asp']

    rules = (
        Rule(LinkExtractor(allow=r'list\.asp\?cid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'article\.asp\?id=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list\.asp\?cid=\d+&Page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div[3]/div[2]/div[1]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[3]/div[2]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="article_p"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
