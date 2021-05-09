# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A544Spider(CrawlSpider):
    name = '544'
    allowed_domains = ['huangzhong.gov.cn']
    start_urls = ['http://www.huangzhong.gov.cn/zwgk.html']

    rules = (
        Rule(LinkExtractor(allow=r'/html/\d+/List\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/\d+/Item\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/\d+/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/webaspx/view_list\.aspx\?portalid=\d+&lmid=\d+&pages=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div/table/tr[3]/td/table/tr[3]/td/table/tr[2]/td/table/tr[2]/td/table/tr[5]/td/table/tr[2]/td/table/tr[2]/td/table/tr/td/table/tr[2]/td').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div/table/tr[3]/td/table/tr[3]/td/table/tr[2]/td/table/tr[2]/td/table/tr[5]/td/table/tr[2]/td/table/tr[1]/td/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/div/table/tr[3]/td/table/tr[3]/td/table/tr[2]/td/table/tr[2]/td/table/tr[5]/td/table/tr[2]/td/table/tr[4]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            print("There have no time format.")
