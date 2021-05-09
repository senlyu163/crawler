# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A498Spider(CrawlSpider):
    name = '498'
    allowed_domains = ['zazf.gov.cn']
    start_urls = [
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=158&catalog_id=158',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=11&catalog_id=11',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=16&catalog_id=16',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=21&catalog_id=21',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=39&catalog_id=39',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=42&catalog_id=42',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=65&catalog_id=65',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=78&catalog_id=78',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=162&catalog_id=162',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=25&catalog_id=25',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=70&catalog_id=70',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=47&catalog_id=47',
        'http://www.zazf.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=47&catalog_id=47',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/gk/.*/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?site_id=CMSza&catalog_id=\d+&cur_page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="contentLeft"]/div[1]/span[2]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="contentLeft"]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="info"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
