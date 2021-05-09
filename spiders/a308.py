# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A308Spider(CrawlSpider):
    name = '308'
    allowed_domains = ['xiaojin.gov.cn']
    start_urls = [
        'http://www.xiaojin.gov.cn/xjxrmzf/c100103/nav_list.shtml',
        'http://www.xiaojin.gov.cn/xjxrmzf/c101902/nav_list.shtml',
        'http://www.xiaojin.gov.cn/xjxrmzf/c100090/zdlyxxgk.shtml',
        # 'http://xiaojin.gov.cn/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/xjxrmzf/c\d+/[a-z]+\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/xjxrmzf/c\d+/\d+/.*\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'nav_list_\d+\.shtml'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="nav_list_nav_main"]/ul[1]//li'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[1]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/div/div[2]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="common_detail"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
