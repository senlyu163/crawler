# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A161Spider(CrawlSpider):
    name = '161'
    allowed_domains = ['jgs.gov.cn']
    start_urls = ['http://www.jgs.gov.cn/node/11.jspx']

    rules = (
        Rule(LinkExtractor(allow=r'/node/\d+\.jspx'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="govpublic"]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/node/\d+_\d+\.jspx'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/label[2]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/div[2]/div[2]/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="info-text nr"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
