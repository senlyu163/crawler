# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A591Spider(CrawlSpider):
    name = '591'
    allowed_domains = ['xjqh.gov.cn']
    start_urls = [
        # 'http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex=1',
        # 'http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex=2',
        # 'http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex=3',
        # 'http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex=4',
        # 'http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex=5',
        'http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex=6',
        'http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex=7',
    ]

    url_nums = 0

    # url_template = "http://www.xjqh.gov.cn/govxxgk/001001/category/001/govlist.html?deptcode=001001&categorynum=001&pageIndex={}"
    # for n in range(229):
    #     url = url_template.format(n+1)
    #     start_urls.append(url)

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@id="govinfolist"]//li'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.url_nums = self.url_nums + 1
        print("@@@@@@@@@@@@@  ", response.url, '    num: ', self.url_nums)
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="container"]/div[3]/div/div/div[1]/table/tr[3]/td[4]/span').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="container"]/div[3]/div/div/div[1]/table/tr[1]/td[2]/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="ewb-article"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
