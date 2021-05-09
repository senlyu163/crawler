# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A383Spider(CrawlSpider):
    name = '383'
    allowed_domains = ['longling.gov.cn']
    start_urls = ['http://www.longling.gov.cn/xxgk.jsp?urltype=tree.TreeTempUrl&wbtreeid=1043']

    rules = (
        Rule(LinkExtractor(allow=r'info/egovinfo/.*\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?totalpage=\d+&PAGENUM=\d+&urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="info"]/span[3]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="title"]/h1/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
