# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A123Spider(CrawlSpider):
    name = '123'
    allowed_domains = ['tangyuan.gov.cn']
    start_urls = [
        'http://tangyuan.gov.cn/government_qu?openCategoryId=61',
    ]

    url_template = "http://tangyuan.gov.cn/government_qu.action?pageInfo.pageSize=20&d=19051509369088413&pageInfo.currentPage={}&pageInfo.pageSize=20"
    for n in range(300):
        url = url_template.format(n+1)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[3]/div[2]/div[2]/ul//li'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/government_qu\.action\?openCategoryId=\d+&d=\d+&pageInfo\.currentPage=\d+&pageInfo\.pageSize=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div/div[3]/div[2]/div[2]/span/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div/div[3]/div[2]/div[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="td2 pt20"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
