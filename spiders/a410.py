# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A410Spider(CrawlSpider):
    name = '410'
    allowed_domains = ['shuangjiang.gov.cn']
    start_urls = [
        'http://www.shuangjiang.gov.cn/shuangjiang/zwgk68/xxgkpt/ysqgk22/index.html',
    ]

    yjsgk = "http://www.shuangjiang.gov.cn/shuangjiang/zwgk68/xxgkpt/yjsgk/c1625677-{}.html"
    for n in range(19):
        url = yjsgk.format(n+1)
        start_urls.append(url)

    tpgj = "http://www.shuangjiang.gov.cn/shuangjiang/zwgk68/tpgj/c1625677-{}.html"
    for n in range(2):
        url = tpgj.format(n+1)
        start_urls.append(url)

    dflzjs = "http://www.shuangjiang.gov.cn/shuangjiang/zwgk68/dflzjs/c1625677-{}.html"
    for n in range(3):
        url = dflzjs.format(n+1)
        start_urls.append(url)

    zcjd = "http://www.shuangjiang.gov.cn/shuangjiang/zwgk68/zcjd0/c1625677-{}.html"
    for n in range(2):
        url = zcjd.format(n+1)
        start_urls.append(url)

    djgz = "http://www.shuangjiang.gov.cn/shuangjiang/zwgk68/djgz3/c1625677-{}.html"
    for n in range(2):
        url = djgz.format(n+1)
        start_urls.append(url)

    jrsj = "http://www.shuangjiang.gov.cn/shuangjiang/zwxx152/jrsj/8684ff62-{}.html"
    for n in range(46):
        url = jrsj.format(n+1)
        start_urls.append(url)

    bmdt = "http://www.shuangjiang.gov.cn/shuangjiang/zwxx152/bmdt8/8684ff62-{}.html"
    for n in range(23):
        url = bmdt.format(n+1)
        start_urls.append(url)

    xzdt = "http://www.shuangjiang.gov.cn/shuangjiang/zwxx152/xzdt22/8684ff62-{}.html"
    for n in range(16):
        url = xzdt.format(n+1)
        start_urls.append(url)

    tzgg = "http://www.shuangjiang.gov.cn/shuangjiang/zwxx152/tzgg32/8684ff62-{}.html"
    for n in range(26):
        url = tzgg.format(n+1)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/shuangjiang/[a-z]+\d+/[a-z]+/[a-z]+\d+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/shuangjiang/.*/\d+/index\.html'), callback='parse_item', follow=True),
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

        contents = response.xpath('//td[@id="xilan_cont"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
