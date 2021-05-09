# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A172Spider(CrawlSpider):
    name = '172'
    allowed_domains = ['yyzfw.gov.cn']
    start_urls = ['http://www.yyzfw.gov.cn/index.php?m=content&c=index&a=lists&catid=28']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="treemenu"]//h3/span'), follow=True),
        Rule(LinkExtractor(allow=r'/index\.php\?m=content&c=index&a=show&catid=\d+&id=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index\.php\?m=content&c=index&a=lists&catid=\d+&page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/p/span/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[1]/p/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="zwtext bordergrey"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
