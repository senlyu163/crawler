# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A126Spider(CrawlSpider):
    name = '126'
    allowed_domains = ['hljlanxi.gov.cn']
    start_urls = ['http://www.hljlanxi.gov.cn/index.php?p=zwgk&biaoti=3&biaoti2=3']

    rules = (
        Rule(LinkExtractor(allow=r'\?p=[a-z]+_list'), follow=True),
        # Rule(LinkExtractor(allow=r'index\.php\?p=[a-z]+_list&c_id=\d+&lanmu=\d+'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="n_newlist"]/ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/index\.php\?p=[a-z]+_list&page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[3]/div[3]/div[2]/div[3]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[3]/div[3]/div[2]/div[1]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="dan_xx"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            print("there have no time.")
