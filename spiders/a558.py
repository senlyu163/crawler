# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
import requests

class A558Spider(CrawlSpider):
    name = '558'
    allowed_domains = ['yanchi.gov.cn']
    start_urls = [
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/xwwj/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/xzfwj/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/bmwj/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/zcjd/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/fgzc/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/yqhy/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/rsxx/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/ghjh/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/hjhly/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/spyp/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/yajyta/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/czzj/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/tjxx/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/shjz/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/zfbz/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/nyxx/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/jyty/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/jyty/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/jycy/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/czgk/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/zfcwhy/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/aqsc/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/jycy_24539/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/zfkfr/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/zfbz/ncwfgz/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/ggwhfw/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/ntsl/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/phqzg/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/jsjf/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/sjgg/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/ssjygk/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/wshjs/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/cpzl/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/gggz/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/hjgl/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/dcjc/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/fpgz/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/yjgl/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/fzzfjs/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/fgzc/gfxwj/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/ghjh/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/xwfbh/list.html',
        'http://www.yanchi.gov.cn/xxgk/zfxxgkml/zsks/list.html',
    ]

###########################################################
    # note this for accelerate scrapy start speed.

    # for su in start_urls:
    #     url_template = su[:-5] + "_{}" + su[-5:]
    #     for n in range(500):
    #         if requests.get(url=url_template.format(n+1)).status_code == int('200'):
    #             start_urls.append(url_template.format(n+1))
    #         else:
    #             break
###########################################################

    # start_urls = ["http://www.yanchi.gov.cn/xxgk/zfxxgkml/list.html"]
    #
    # url_template = "http://www.yanchi.gov.cn/xxgk/zfxxgkml/list_{}.html"
    # for n in range(49):
    #     url = url_template.format(n+1)
    #     start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[5]/div/div/div/div[3]/table/tbody/tr[1]/td[3]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[5]/div/div/div/div[2]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="zz-xl-ct"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
