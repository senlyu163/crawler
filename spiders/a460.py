# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A460Spider(CrawlSpider):
    name = '460'
    allowed_domains = ['heyang.gov.cn']
    start_urls = ['http://www.heyang.gov.cn/2018zwgk_list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1047']

    rules = (
        Rule(LinkExtractor(allow=r'/\d+zwgk_list\.jsp\?urltype=tree\.TreeTempUrl&wbtreeid=\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/gk/[a-z]+/[a-z]+/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+\.htm$'), follow=True),
        Rule(LinkExtractor(allow=r'/info/\d+/\d+\.htm'), callback='parse_item_1', follow=True),
        Rule(LinkExtractor(allow=r'[a-z]+/\d+\.htm$'), follow=True),
        Rule(LinkExtractor(allow=r'\?totalpage=\d+&PAGENUM=\d+&urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="cj2"]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[4]/div[4]/table/tbody/tr[3]/td[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="infoContent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def parse_item_1(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[7]/form/div/h2').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[7]/form/div/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="vsb_content_2"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item