# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A231Spider(CrawlSpider):
    name = '231'
    allowed_domains = ['gdx.gov.cn']
    start_urls = [
        'http://www.gdx.gov.cn/20330/',
        'http://www.gdx.gov.cn/20330/20409/20410/index.htm',
        'http://www.gdx.gov.cn/20330/20409/20415/index.htm',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="down-menu down-menu2"]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="more"]'), follow=True),
        Rule(LinkExtractor(allow=r'content_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.htm'), follow=True),
        Rule(LinkExtractor(allow=r'\d+/index\.htm'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[5]/div[4]/span[1]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[5]/div[2]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="xl-content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[2]/text()').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('//div[@class="title"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
