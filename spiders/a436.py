# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A436Spider(CrawlSpider):
    name = '436'
    allowed_domains = ['ws.yn.gov.cn']
    start_urls = ['http://www.ws.yn.gov.cn/dlwsrmzfmh/5404897895960805376/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/dlwsrmzfmh/\d+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/dlwsrmzfmh/\d+/\d+/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\d+_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        # date = response.xpath('//div[@class="detail"]/div[1]').extract_first()
        # date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        # item['date'] = date

        url = response.url
        idx = url.rfind('/')
        date = url[idx - 8:idx]
        date_format = date[:4] + '-' + date[4:6] + '-' + date[6:]
        item['date'] = date_format

        title = response.xpath('/html/body/div/table[2]/tr/td/table/tr/td/div/table/tr/td/div/table/tr/td/div/table/tr[3]/td/div/table/tr/td/font/b/text()').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/div/table[2]/tr/td/table/tr/td/div/table/tr/td/div/table/tr/td/div/table/tr[3]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
