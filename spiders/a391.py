# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A391Spider(CrawlSpider):
    name = '391'
    allowed_domains = ['suijiang.gov.cn']
    start_urls = ['http://www.suijiang.gov.cn/subsiteIndex/toPage?subsiteFlag=suijiangpc&subsiteId=1&newsClassId=114&pageType=auto&pageSize=20&start=0&objectId=']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//dl[@class="leftNav_dl"]//dd'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//dl[@class="leftNav_dl"]//dd/div/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//dl[@class="infoOpen_dl"]//dd/div'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/subsiteIndex/toPage\?subsiteFlag=suijiangpc&subsiteId=\d+&newsClassId=\d+&pageType=auto&pageSize=\d+&start=\d+&objectId=$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="articleOhter"]/div[1]/div[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="articleTitle"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="articleBox"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
