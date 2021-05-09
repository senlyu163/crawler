# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re


class A158Spider(CrawlSpider):
    name = '158'
    allowed_domains = ['suichuan.gov.cn']
    start_urls = [
        'http://www.suichuan.gov.cn/xxgk/ghjh/gmjjhshfzgh/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/tjxx/tjgb/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/czxx/czyjs/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/zfcg/zfjzcgml/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/yjgl/yjzs/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/jytabl/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/ggjg/aqsc/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/rsxx/rsrm/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/ggzypz/zdxm/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/shgl/fpkf/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/tdcr/index.shtml',
        'http://www.suichuan.gov.cn/xxgk/zcfg/xgfxwj/index.shtml',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="font20"]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="rightCon fr"]/div[1]/ul[1]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/xxgk/[a-z]+/index_\d+\.shtml'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[4]/div[3]/div/div/p/text()[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[4]/div[3]/div/div/h3/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="Zoom"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
