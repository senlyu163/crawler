# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A447Spider(CrawlSpider):
    name = '447'
    allowed_domains = ['zf.xgll.gov.cn']
    start_urls = [
        'http://zf.xgll.gov.cn/html/zf_zwdt/zf_zwdt_yw/',
        'http://zf.xgll.gov.cn/html/zf_zcfg/',
        'http://zf.xgll.gov.cn/html/zf_zfjg/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/html/\d+/.*/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/zf_zwdt/zf_zwdt_yw/\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/zf_zcfg/\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/zf_zfjg/zf_zfjg_zsbm/zf_zfjg_zs_[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="moreright1"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/zf_zfjg/.*/\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div/div/div[3]/div[1]/div[3]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div/div/div[3]/div[1]/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/div/div/div[3]/div[1]/div[4]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
