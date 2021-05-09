# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A465Spider(CrawlSpider):
    name = '465'
    allowed_domains = ['yanchangxian.gov.cn']
    start_urls = ['http://www.yanchangxian.gov.cn/overt_list_bm.jsp?urltype=tree.TreeTempUrl&wbtreeid=1310']

    rules = (
        Rule(LinkExtractor(allow=r'overt_list\.jsp\?urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'overt_list\d+_doucment\.jsp\?urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'info/egovinfo/.*/\d+-\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?totalpage=\d+&PAGENUM=\d+&urltype=tree\.TreeTempUrl&wbtreeid=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div/div[2]/div/div[1]/table/tr[2]/td[2]').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div/div[2]/div/div[1]/table/tr[3]/td/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="vsb_content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
