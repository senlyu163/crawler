# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A306Spider(CrawlSpider):
    name = '306'
    allowed_domains = ['xxgk.scnj.gov.cn']
    start_urls = ['http://xxgk.scnj.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'index\.aspx\?gpiid=\d+&dept=\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/t\.aspx\?i=\d+-\d+-\d+-\d+$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index\.aspx\?p=\d+&gpiid=&dept=\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'GPI/index\.aspx\?dept=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="form1"]/div[2]/table[4]/tr/td/table/tr/td[2]/table/tr[2]/td/table/tr/td/table[1]/tr/td/table/tr[2]/td[1]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="form1"]/div[2]/table[4]/tr/td/table/tr/td[2]/table/tr[2]/td/table/tr/td/table[3]/tr/td/table/tr/td/table[1]/tr[1]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="form1"]/div[2]/table[4]/tr/td/table/tr/td[2]/table/tr[2]/td/table/tr/td/table[3]/tr/td/table/tr/td/table[1]/tr[3]').extract()
        item['contents'] = extract_CN_from_content(contents)

        year = date[:4]
        if int(year) >= 2015 and int(year) <= 2019:
            return item
