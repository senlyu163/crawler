# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A566Spider(CrawlSpider):
    name = '566'
    allowed_domains = ['xjblk.gov.cn']
    start_urls = [
        'http://www.xjblk.gov.cn/2018_moban/index18_2D.jsp?urltype=tree.TreeTempUrl&wbtreeid=1062',
        'http://www.xjblk.gov.cn/2018_moban/index18_2D_DiR.jsp?urltype=tree.TreeTempUrl&wbtreeid=1202'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/\d+_moban/index\d+_\d+C_LiST\.jsp\?urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+_moban/index\d+_\d+D_DiR_LiST\.jsp\?urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/2018_moban/index\d+_\d+D_DETAiL\.jsp\?urltype=egovinfo\.EgovInfoContent'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?ainfolist\d+t=\d+&ainfolist\d+p=\d+&ainfolist\d+c=\d+&urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="time"]').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/table/tr[1]/td/table/tr[1]/td/div/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="egovinfocontenttable"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
