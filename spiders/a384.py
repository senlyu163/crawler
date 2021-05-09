# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A384Spider(CrawlSpider):
    name = '384'
    allowed_domains = ['yncn.gov.cn']
    start_urls = ['http://www.yncn.gov.cn/xxgklmy.jsp?urltype=tree.TreeTempUrl&wbtreeid=1267']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="tablebody"]//div/div[1]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?totalpage=\d+&PAGENUM=\d+&urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div/table/tr[1]/td/table/tr[2]/td/table/tr[1]/td[6]').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div/table/tr[1]/td/table/tr[1]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="egovinfocontenttable"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
