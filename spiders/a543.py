# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A543Spider(CrawlSpider):
    name = '543'
    allowed_domains = ['datong.gov.cn']
    start_urls = ['http://www.datong.gov.cn/index.php?s=news&c=category&id=13']

    rules = (
        Rule(LinkExtractor(allow=r'/index\.php\?s=news&c=category&id=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/index\.php\?s=news&c=show&id=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/index\.php\?s=news&c=category&id=\d+&page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div/div[2]/div/div[2]/div[1]/div/div/table/tbody/tr[2]/td[2]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div/div[2]/div/div[2]/div[1]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="dfz-xl-sp"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
