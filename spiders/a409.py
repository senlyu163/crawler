# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A409Spider(CrawlSpider):
    name = '409'
    allowed_domains = ['ynzk.gov.cn']
    start_urls = [
        'http://www.ynzk.gov.cn/zhenkan/xxgk56/zfwj0/zfwj1537/index.html'
    ]

    zfwj = "http://www.ynzk.gov.cn/zhenkan/xxgk56/zfwj0/zfwj1537/b0c372c0-{}.html"
    for n in range(3):
        url = zfwj.format(n+1)
        start_urls.append(url)

    zcjd = "http://www.ynzk.gov.cn/zhenkan/xxgk56/zcjd66/0b45954c-{}.html"
    for n in range(3):
        url = zcjd.format(n+1)
        start_urls.append(url)

    jyta = "http://www.ynzk.gov.cn/zhenkan/xxgk56/jyta25/b0458810-{}.html"
    for n in range(13):
        url = jyta.format(n+1)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/zhenkan/[a-z]+\d+/[a-z]+\d+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/zhenkan/.*/\d+/index\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="xilan_tab"]/tbody/tr[5]/td/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//h1[@id="jiuctit"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="cont_len"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item