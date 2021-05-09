# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A297Spider(CrawlSpider):
    name = '297'
    allowed_domains = ['jialing.gov.cn']
    start_urls = [
        'http://www.jialing.gov.cn/a/sjzt/gongzuodongtai/',
        'http://www.jialing.gov.cn/a/xxgk/zhengwudongtai/',
        'http://www.jialing.gov.cn/a/czzj/ysjs/',
        'http://www.jialing.gov.cn/a/xxgk/zhongdianxinxigongkai/zdlygk/',
        'http://www.jialing.gov.cn/a/sjzt/gongzuodongtai/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="menuList"]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="newsList"]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list_\d+_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="content"]/div/article/div/div[1]/span[3]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="content"]/div/article/div/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="conTxt"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
