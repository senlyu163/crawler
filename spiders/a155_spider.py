# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A155_spiderSpider(scrapy.Spider):
    name = '155_spider'
    allowed_domains = ['huichang.gov.cn']
    start_urls = ['http://www.huichang.gov.cn/jsearchfront/categorySearch.do?websiteid=360733000000000&cateid=3&ranksign=&p=1&pg=&total=73326&tpl=10&searchid=1&pos=title&q=&pq=&oq=&eq=']

    web_head_domain = 'http://www.huichang.gov.cn/jsearchfront/categorySearch.do?websiteid=360733000000000&cateid=3&ranksign=&p={}&pg=&total=73326&tpl=10&searchid=1&pos=title&q=&pq=&oq=&eq='

    def parse(self, response):
        # table_urls = response.xpath('//div[@class="news-type"]//div/div[1]/a/@href').extract()
        # for tu in table_urls:
        #     print("$$ ", tu)
        # search_page_num = 10
        # for page_num in range(search_page_num):
        #     complete_url = self.web_head_domain.format(page_num+1)
        #     yield SplashRequest(url=complete_url, callback=self.extract_table_url, args={"wait": 0.5})

        yield SplashRequest(url=response.url, callback=self.extract_table_url, args={"wait": 0.5})

    def extract_table_url(self, response):
        table_urls = response.xpath('//div[@class="news-type"]//div/div[1]/a/@href').extract()
        web_domain = 'http://www.huichang.gov.cn/jsearchfront/'
        for tu in table_urls:
            complete_url = web_domain + tu
            yield scrapy.Request(url=complete_url, callback=self.extract_content)

    def extract_content(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div/div[2]/div/div/div[1]/ul/li[6]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/div/div[2]/div/div/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="counts_news"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item