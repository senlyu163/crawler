# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A406Spider(CrawlSpider):
    name = '406'
    allowed_domains = ['ynfq.gov.cn']

    start_urls = [
        'http://www.ynfq.gov.cn/fqxrmzf/zdlygk2/zfcg78/index.html'
    ]

    czxx = "http://www.ynfq.gov.cn/eportal/ui?pageId=56343&currentPage={}&moduleId=37611fb90c864677be6f51b5eef91191&staticRequest=yes"
    for n in range(19):
        url = czxx.format(n+1)
        start_urls.append(url)

    fpgz = "http://www.ynfq.gov.cn/fqxrmzf/zdlygk2/fpgzxx57/47aa6026-{}.html"
    for n in range(5):
        url = fpgz.format(n+1)
        start_urls.append(url)

    acjd = "http://www.ynfq.gov.cn/fqxrmzf/xxgk72/zcjd96/be2d9e09-{}.html"
    for n in range(3):
        url = acjd.format(n+1)
        start_urls.append(url)

    czyjs = "http://www.ynfq.gov.cn/eportal/ui?pageId=56153&currentPage={}&moduleId=be2d9e0953dc4ef791b001eb738f805b&staticRequest=yes"
    for n in range(15):
        url = czyjs.format(n+1)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/fqxrmzf/[a-z]+\d+/[a-z]+\d+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/fqxrmzf/.*/\d+/index\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
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
