# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
import requests

class A564Spider(CrawlSpider):
    name = '564'
    allowed_domains = ['pengyang.gov.cn']
    start_urls = [
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/xzfwj/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/wjfb/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/zcjd/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/czzj/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/ta/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/zdcq/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/xzqlyx/ssj/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/ghjh/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/zfbz/wywfgz/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/tjxx/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/jg_39822/zsks/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/zdlyxx/jy/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/jg_39822/yl/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/xzjgjc/sp/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/zdlyxx/hjgl/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/xzjgjc/aq/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/zfbz/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/zdlyxx/yj/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/jg_39822/shjz/list.html',
        'http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/jg_39822/hjbh/list.html',
    ]

################################################
    # note this for accelerate scrapy start speed.

    # for su in start_urls:
    #     url_template = su[:-5] + "_{}" + su[-5:]
    #     for n in range(500):
    #         if requests.get(url=url_template.format(n+1)).status_code == int('200'):
    #             start_urls.append(url_template.format(n+1))
    #         else:
    #             break
################################################

    # url_template = "http://www.pengyang.gov.cn/xxgk_13872/zfxxgkml/list_{}.html"
    # for n in range(49):
    #     url = url_template.format(n+1)
    #     start_urls.append(url)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="boxcon"]//div/ul/li[2]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div[4]/div[3]/table/tbody/tr[1]/td[3]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[4]/div[2]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="zz-xl-sec"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
