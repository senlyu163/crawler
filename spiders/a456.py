# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A456Spider(CrawlSpider):
    name = '456'
    allowed_domains = ['yongshou.gov.cn']
    start_urls = ['http://www.yongshou.gov.cn/html/zwgk/xxgkml/czxx/czxx/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/news_list\.rt\?channlId=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/html/zwgk/xxgkml/[a-z]+/index.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/[a-z]+/[a-z]+/\d+/\d+\.html'), callback='parse_item_1', follow=True),
        Rule(LinkExtractor(allow=r'/news_list\.rt\?channlId=\d+&pageNo=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'/html/[a-z]+/[a-z]+/[a-z]+/[a-z]+/\d+/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/zwgk/xxgkml/[a-z]+/\d+/\d+\.html'), callback='parse_item', follow=True),

        # Rule(LinkExtractor(allow=r'/news_list\.rt\?channlCid=.*pageNo=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/news_list\.rt\?channlCid=\d+&channlId=\d+&pageNo=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print("############### ", response.url)
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[5]/div/div[1]/table/tr[2]/td[6]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="zwgkdetailpart2_bt"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="zwgkdetailpart2_nr"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def parse_item_1(self, response):
        # print("!!!!!!!!!!!!!!!!!!  ", response.url)
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="newdetailpart_fbsj"]/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="newdetailpart_bt"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="newdetailpart_nr"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
