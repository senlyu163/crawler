# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A553Spider(CrawlSpider):
    name = '553'
    allowed_domains = ['maduo.gov.cn']
    start_urls = ['http://www.maduo.gov.cn/html/2160/List.html']

    rules = (
        Rule(LinkExtractor(allow=r'/html/\d+/List\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/\d+/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/webaspx/view_list\.aspx\?portalid=\d+&lmid=\d+&pages=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div/table/tr/td/table/tr[1]/td[3]/table/tr[4]/td/table/tr/td/table/tr/td/table/tr[3]/td/table/tr/td/table/tr[4]/td/table/tr/td').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div/table/tr/td/table/tr[1]/td[3]/table/tr[4]/td/table/tr/td/table/tr/td/table/tr[3]/td/table/tr/td/table/tr[2]/td/span/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/div/table/tr/td/table/tr[1]/td[3]/table/tr[4]/td/table/tr/td/table/tr/td/table/tr[3]/td/table/tr/td/table/tr[6]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="table568"]/tr/td/font').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="table567"]/tr[1]/td/font/span/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="txtcen"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
