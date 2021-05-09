# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
import requests

class A562Spider(CrawlSpider):
    name = '562'
    allowed_domains = ['nxld.gov.cn']
    start_urls = [
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zdgc/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/rdhy/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zfwj/list.html',
        'http://www.nxld.gov.cn/xxgk/zfgzbg/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/xzqlyx/xzcf/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/xzqlyx/xzxk/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zfgb/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zcfg/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zfwj/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/rdhy/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/czzj/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zdgc/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/slsb/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zfcwgzhy/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/tjxx/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/ghjh/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zxjf/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/shgysyjs/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/yata/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/jdjcjzg/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/jycy/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/xzqlyx/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/flfw/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/szfw/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/jtys/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/zfkfrhd/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/nync/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/jsjf/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/kjfw/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/stly/list.html',
        'http://www.nxld.gov.cn/xxgk/zfxxgkml/sjgk/list.html',
    ]

#########################################################
    # note this for accelerate scrapy start speed.

    # for su in start_urls:
    #     url_template = su[:-5] + "_{}" + su[-5:]
    #     for n in range(500):
    #         if requests.get(url=url_template.format(n+1)).status_code == int('200'):
    #             start_urls.append(url_template.format(n+1))
    #         else:
    #             break
    #####################################################

    # start_urls = ["http://www.nxld.gov.cn/xxgk/zfxxgkml/list.html"]
    #
    # url_template = "http://www.nxld.gov.cn/xxgk/zfxxgkml/list_{}.html"
    #
    # for n in range(49):
    #     url = url_template.format(n+1)
    #     start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[1]/td[3]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[3]/div[2]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="zz-xl-ct"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
