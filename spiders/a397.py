# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A397Spider(CrawlSpider):
    name = '397'
    allowed_domains = ['ne.gov.cn']
    start_urls = ['http://www.ne.gov.cn/xxgk_list.jsp?urltype=egovinfo.EgovInfoList&wbtreeid=1036&sccode=ne&subtype=1&dpcode=P010&gilevel=1']

    rules = (
        Rule(LinkExtractor(allow=r'info/egovinfo/\d+/xxgk_content/.*\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?ainfolist\d+t=\d+&ainfolist\d+p=\d+&ainfolist\d+c=\d+&urltype=egovinfo\.EgovInfoList&wbtreeid=\d+&sccode=ne&subtype=\d+&dpcode=P\d+&gilevel=\d+$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div/div/div[2]/div/div/table/tr[1]/td/table/tr[2]/td/table/tr[1]/td[6]').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div/div/div[2]/div/div/table/tr[1]/td/table/tr[1]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="egovinfocontenttable"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item