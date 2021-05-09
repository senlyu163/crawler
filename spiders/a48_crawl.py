# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re

class A48CrawlSpider(CrawlSpider):
    name = '48_crawl'
    allowed_domains = ['wuxiang.gov.cn']
    start_urls = ['http://www.wuxiang.gov.cn/wxxxgk/zfxxgk/bmxxgk/']

    rules = (
        Rule(LinkExtractor(allow=r'/[a-z]+/chnlnull_\d+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/chnl\d+/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[5]/div/div/div[1]/table/tr[5]/td[2]/span[3]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[5]/div/div/div[1]/table/tr[4]/td/span[3]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="article-con TRS_Editor"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
