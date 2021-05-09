# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A222Spider(CrawlSpider):
    name = '222'
    allowed_domains = [
        'hfweb.cn',
        'http://hflz.hfweb.cn/'
    ]
    start_urls = [
        'http://www.hfweb.cn/Category_3422/Index.aspx',
        'http://www.hfweb.cn/Category_3442/Index.aspx',
        'http://www.hfweb.cn/Category_3454/Index.aspx',

        'http://hflz.hfweb.cn/Category_4065/Index.aspx',
        'http://hflz.hfweb.cn/Category_1156/Index.aspx',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/Item/\d+\.aspx'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'Index_\d+\.aspx'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="wenzhang"]/div[1]/text()[1]').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="d_picTit"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="wzcon articleCon"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="content"]/div[2]/div/div/div[1]/span[3]/text()').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="d_picTit"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="conTxt"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
