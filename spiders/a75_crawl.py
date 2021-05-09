# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A75CrawlSpider(CrawlSpider):
    name = '75_crawl'
    allowed_domains = ['wuchuan.gov.cn']
    start_urls = ['http://www.wuchuan.gov.cn/zfxxgkpt/xxgkml/index_2387.html']

    url_template = "http://www.wuchuan.gov.cn/zfxxgkpt/xxgkml/index_2387_{}.html"
    for n in range(66):
        url = url_template.format(n+1)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//table[@class="xxgk_info"]/tr[2]/td[3]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//table[@class="xxgk_info"]/tr[1]/td[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="para"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
