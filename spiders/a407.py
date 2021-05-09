# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A407Spider(CrawlSpider):
    name = '407'
    allowed_domains = ['ynyx.gov.cn']
    start_urls = [
        'http://www.ynyx.gov.cn/yxrmzf/xxgk4/zfwj72/zfwj74/index.html',
        'http://www.ynyx.gov.cn/yxrmzf/zdlygk66/czxx25/czyjs57/2e578dc7-2.html',
    ]

    czyjs = "http://www.ynyx.gov.cn/yxrmzf/zdlygk66/czxx25/czyjs57/2e578dc7-{}.html"
    for n in range(7):
        url = czyjs.format(n+1)
        start_urls.append(url)

    sgjf = "http://www.ynyx.gov.cn/yxrmzf/zdlygk66/czxx25/sgjf4016/2e578dc7-{}.html"
    for n in range(2):
        url = sgjf.format(n+1)
        start_urls.append(url)

    fpzj = "http://www.ynyx.gov.cn/yxrmzf/zdlygk66/czxx25/216313/aac6a7eb-{}.html"
    for n in range(3):
        url = fpzj.format(n+1)
        start_urls.append(url)

    zfwj = "http://www.ynyx.gov.cn/yxrmzf/xxgk4/zfwj72/zfwj74/2e578dc7-{}.html"
    for n in range(2):
        url = zfwj.format(n+1)
        start_urls.append(url)

    zfbz = "http://www.ynyx.gov.cn/yxrmzf/zdlygk66/zfbzxx71/2e578dc7-{}.html"
    for n in range(3):
        url = zfbz.format(n+1)
        start_urls.append(url)

    scjg = "http://www.ynyx.gov.cn/yxrmzf/zdlygk66/scjgxx/2e578dc7-{}.html"
    for n in range(3):
        url = scjg.format(n+1)
        start_urls.append(url)

    gsgg = "http://www.ynyx.gov.cn/yxrmzf/zdlygk66/gytdxx54/gsgg64/2e578dc7-{}.html"
    for n in range(9):
        url = gsgg.format(n+1)
        start_urls.append(url)

    jyta = "http://www.ynyx.gov.cn/yxrmzf/zdlygk66/159717/2e578dc7-{}.html"
    for n in range(5):
        url = jyta.format(n+1)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/yxrmzf/[a-z]+\d+/[a-z]+\d+/[a-z]+\d+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/yxrmzf/.*/\d+/index\.html'), callback='parse_item', follow=True),
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
