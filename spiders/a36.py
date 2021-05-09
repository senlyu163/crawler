# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re
from scrapy_splash import SplashRequest

class A36Spider(CrawlSpider):
    name = '36'
    allowed_domains = ['xxgk.hengshui.gov.cn']
    start_urls = ['http://xxgk.hengshui.gov.cn/eportal/ui?pageId=793450']


    # url_template = "http://xxgk.hengshui.gov.cn/eportal/ui?pageId=793450&currentPage={}&moduleId=9757&formKey=GOV_OPEN&columnName=EXT_STR7&relationId="
    # url_template = "http://xxgk.hengshui.gov.cn/eportal/ui?pageId=2668536&currentPage={}&moduleId=55c65eac3ad44c0da4e125f94c8d0b4f&formKey=GOV_OPEN&columnName=EXT_STR7&relationId="
    # for n in range(1148):
    #     url = url_template.format(n+1)
    #     start_urls.append(url)

    rules = (
        # Rule(LinkExtractor(allow=r'\?pageId=\d+.*columnId=\d+'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'//*[@id=".*"]/div[2]/div/table[2]/tbody/tr[\d+]/td/table/tbody/tr[\d+]/td/table/tbody/tr/td[\d+]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/body/div[3]/div[2]/div/div[3]/div/div[2]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[.*]/td/table/tbody/tr/td[2]/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/html/body/div[3]/div[2]/div/div[3]/div/div[2]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/body/div[3]/div[2]/div/div[3]/div/div[2]/div/table[2]/tbody/tr[2]/td/div/ul[1]/li[3]/a'), callback='start_requests', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        for url in self.start_urls:
            # Splash 默认是render.html,返回javascript呈现页面的HTML。
            yield SplashRequest(url, args={'wait': 1})

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[5]/div/div/div/div[2]/div[1]/table/tbody/tr[3]/td[4]').extract_first()
        # date = response.xpath('//*[@id="c5b5bea019d64dfda1026231af61f5e2"]/div[2]/div[1]/table/tbody/tr[3]/td[4]').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        # title = response.xpath('//*[@id="c5b5bea019d64dfda1026231af61f5e2"]/div[2]/div[1]/table/tbody/tr[1]/td[2]/text()').extract_first()
        title = response.xpath('/html/body/div[5]/div/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]').extract_first()
        item['title'] = title

        # contents = response.xpath('//*[@id="c5b5bea019d64dfda1026231af61f5e2"]/div[2]/div[3]').extract()
        contents = response.xpath('/html/body/div[5]/div/div/div/div[2]/div[3]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
