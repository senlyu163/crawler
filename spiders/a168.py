# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A168Spider(CrawlSpider):
    name = '168'
    allowed_domains = ['lankao.gov.cn']
    start_urls = ['http://www.lankao.gov.cn/zwgk/zfbmxxgk.htm']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ol[@class="xxgk_menu"]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="_list"]/table//tr/td[2]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?totalpage=\d+&PAGENUM=\d+&urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'\?urltype=egovinfo\.EgovTreeURl&wbtreeid=\d+&type=egovinfodeptsubcattree&sccode=zyzz&subtype=\d+&dpcode=fpb&gilevel=\d+'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="com_list"]//li'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="printCont"]/div[1]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="printCont"]/h1/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="texts"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
