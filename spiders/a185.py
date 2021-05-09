# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A185Spider(CrawlSpider):
    name = '185'
    allowed_domains = ['suixian.gov.cn']
    start_urls = ['http://suixian.gov.cn/index/information/xxgk.html',
                  'http://suixian.gov.cn/index/information/xxgk_zdly1/id/63.html']

    rules = (
        Rule(LinkExtractor(allow=r'/index/information/xxgk_list/id/\d+\.html$'), follow=True),
        Rule(LinkExtractor(allow=r'/index/index/detail/id/\d+/type/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/index/information/xxgk_list/id/\d+\.html\?page=\d+'), follow=True),

        Rule(LinkExtractor(allow=r'/xxgk_[a-z]+/class_id/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/index/information/xxgk_[a-z]+/class_id/\d+\.html\?page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/index/information/xxgk_[a-z]+/class_id/\d+/id/\d+\.html$'), follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div[2]/div[1]/span[2]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/div[2]/h3/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="newsContent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
