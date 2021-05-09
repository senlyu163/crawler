# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A143Spider(CrawlSpider):
    name = '143'
    allowed_domains = ['shucheng.gov.cn']
    start_urls = [
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466a3&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466a4&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466a5&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466a6&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466a7&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466a8&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466a9&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466aa&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466ab&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466ac&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466ad&tag=&open_type=',
        'http://www.shucheng.gov.cn/opennessTarget/?branch_id=5bf2d16cb49430e63bc87ef6&branch_type=&column_code=&topic_id=5bfd3d1dd727c90be9c466ae&tag=&open_type=',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="xxgk_navli"]/ul//li[3]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/opennessTarget/\?branch_id=.*&branch_type=&column_code=&topic_id=.*&tag=&open_type=&page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="wenzhang"]/div[1]/table/tbody/tr[2]/td[2]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="wenzhang"]/div[1]/table/tbody/tr[5]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="wenzhang"]/div[3]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
