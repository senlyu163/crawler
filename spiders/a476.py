# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A476Spider(CrawlSpider):
    name = '476'
    allowed_domains = ['hszf.gov.cn']
    start_urls = ['http://www.hszf.gov.cn/info/iList.jsp?cat_id=10015']

    rules = (
        Rule(LinkExtractor(allow=r'/info/iList\.jsp\?cat_id=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/[a-z]+/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?cat_id=\d+&cur_page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="printContent"]/div[6]/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="printContent"]/div[3]/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="m-ct-artcle"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
