# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A135Spider(CrawlSpider):
    name = '135'
    allowed_domains = ['xxgk.ahys.gov.cn']
    start_urls = ['http://xxgk.ahys.gov.cn/opennessTarget/?branch_id=57ec8b1c538739ee34a0cd80&column_code=10000&tag=&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'/openness/detail/content/.*\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/opennessTarget/\?branch_id=.*&column_code=\d+&tag=&page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div/div[2]/table/tr[4]/td[2]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div/div[2]/table/tr[6]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="m-article"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
