# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A107Spider(CrawlSpider):
    name = '107'
    allowed_domains = ['jlzhenlai.gov.cn']
    start_urls = ['http://www.jlzhenlai.gov.cn/xxgk/']

    rules = (
        Rule(LinkExtractor(allow=r'/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[8]/div/div[1]/div[2]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )


    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//div[@class="row_t_content_time_left"]/span[1]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//div[@class="row_t_content_con_title"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="TRS_Editor"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            print("have format error.")
