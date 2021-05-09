# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A302Spider(CrawlSpider):
    name = '302'
    allowed_domains = ['guanganqu.gov.cn']
    start_urls = [
        'http://www.guanganqu.gov.cn/gaqrmzf/zdjc/wgk.shtml',
        'http://www.guanganqu.gov.cn/gaqrmzf/c100056/nav_list.shtml',
        'http://www.guanganqu.gov.cn/gaqrmzf/c100078/nav_list.shtml',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="fl-main"]//ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="fl-main"]//li'), follow=True),
        Rule(LinkExtractor(allow=r'/content_.*\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'wgk_\d+\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'nav_list_\d+\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div/ul[1]/li[1]/span').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/div/div[2]/div[1]/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="d_center"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
