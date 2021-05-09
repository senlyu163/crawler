# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re


class A128Spider(CrawlSpider):
    name = '128'
    allowed_domains = ['qss.gov.cn']
    start_urls = ['https://xxgk.qss.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'https://www\.qss\.gov\.cn/index\.php\?m=content&c=index&a=lists&catid=\d+&sid=\d+&cates=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'https://www\.qss\.gov\.cn/index\.php\?m=content&c=index&a=show&catid=\d+&id=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index\.php\?m=content&c=index&a=lists&catid=\d+&page=\d+&sid=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="container"]/div/div[2]/table/tbody/tr[3]/td[4]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="container"]/div/div[2]/table/tbody/tr[6]/td[2]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="is-content-detail"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="zoomsubtitl"]/table/tr/td/span[2]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="zoomtitl"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@id="zoomcon"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
