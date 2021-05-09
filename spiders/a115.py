# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A115Spider(CrawlSpider):
    name = '115'
    allowed_domains = ['tailai.gov.cn']
    start_urls = ['http://www.tailai.gov.cn/pages/5a6a7acfb3e9411ea4adfec0']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="yiji"]//li//ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="zfwj_content"]//ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div/div[2]/div[3]/nav/div[5]'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="content_part_b_fwrq_content"]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="content_part_b_bt_content"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content_part_d article-margin-bottom"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
