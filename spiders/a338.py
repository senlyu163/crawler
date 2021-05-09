# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A338Spider(CrawlSpider):
    name = '338'
    allowed_domains = ['jiangkou.gov.cn']
    start_urls = ['http://www.jiangkou.gov.cn/xxgk/xxgkml/jcgk/jgsz/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/xxgk/xxgkml/.*/$'), follow=True),
        Rule(LinkExtractor(allow=r'/xxgk/xxgkml/.*\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[4]/div[2]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[4]/div[1]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
