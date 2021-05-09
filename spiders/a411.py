# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A411Spider(CrawlSpider):
    name = '411'
    allowed_domains = ['cangyuan.gov.cn']
    start_urls = ['http://www.cangyuan.gov.cn/cyxrmzf/zwgk49/gggs71/index.html']

    gsgg = "http://www.cangyuan.gov.cn/cyxrmzf/zwgk49/gggs71/1d9826e9-{}.html"
    for n in range(11):
        url = gsgg.format(n+1)
        start_urls.append(url)

    cyxw = "http://www.cangyuan.gov.cn/cyxrmzf/zwgk49/cyxw/1d9826e9-{}.html"
    for n in range(14):
        url = cyxw.format(n+1)
        start_urls.append(url)

    bmdt = "http://www.cangyuan.gov.cn/cyxrmzf/zwgk49/bmdt31/1d9826e9-{}.html"
    for n in range(47):
        url = bmdt.format(n+1)
        start_urls.append(url)

    xzdt = "http://www.cangyuan.gov.cn/cyxrmzf/zwgk49/xzdt6/1d9826e9-{}.html"
    for n in range(42):
        url = xzdt.format(n+1)
        start_urls.append(url)

    lcyw = "http://www.lincang.gov.cn/lcsrmzf/lcszf/zwdt/lcyw/3d5c738e-{}.html"
    for n in range(103):
        url = lcyw.format(n+1)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/cyxrmzf/[a-z]+\d+/\d+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/cyxrmzf/.*/\d+/index\.html'), callback='parse_item', follow=True),
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