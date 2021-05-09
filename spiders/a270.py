# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A270Spider(CrawlSpider):
    name = '270'
    allowed_domains = ['longzhou.gov.cn']
    start_urls = [
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/zfwj',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/zcjd',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/ghjh',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/jgsz',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/rsxx',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/tjxx',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/cfxx',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/sjkf',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/jytabljggs',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/qtxx',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/jsjf',
        'http://www.longzhou.gov.cn/ztzl/tpgj',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/shjz',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/fdcxx',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/hjbh',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/jghsfxx',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/scjg',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/aqsc',
        'http://www.longzhou.gov.cn/ztzl/spypaq',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/ggwhty',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/ylws',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/sjccsxqd',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/jysy',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/zdjsxm',
        'http://www.longzhou.gov.cn/zwgk/zfxxgkml/tdgy',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/zfxxgkml/[a-z]+__[a-z]+/\d+$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/.*/[a-z]+/\d+$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/zfxxgkml/[a-z]+_\d+$'), follow=True),

        Rule(LinkExtractor(allow=r'/content_\d+$'), callback='parse_item_2', follow=True),
        Rule(LinkExtractor(allow=r'/[a-z]+_\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="content"]/div/table/tbody/tr[2]/td[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="content"]/div/div[1]/h3/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="govIntro"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
