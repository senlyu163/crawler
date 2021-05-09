# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A285Spider(CrawlSpider):
    name = '285'
    allowed_domains = ['wush.cq.gov.cn']
    start_urls = ['http://wush.cq.gov.cn/xxgk.htm']

    rules = (
        Rule(LinkExtractor(allow=r'[a-z]+/[a-z]+\.htm$'), follow=True),
        Rule(LinkExtractor(allow=r'/info/\d+/\d+\.htm$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'[a-z]+/\d+\.htm$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[7]/div[1]/form/div[1]/div[1]/text()[1]').extract_first()
        date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="vsb_content_1001"]/div/p[1]/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="v_news_content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
