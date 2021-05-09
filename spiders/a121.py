# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A121Spider(CrawlSpider):
    name = '121'
    allowed_domains = ['huanan.gov.cn']
    start_urls = ['http://www.huanan.gov.cn/find.html?content=&web_id=1&menu_id=4']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="panel_body_content"]/ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/find\.html\?web_id=1&menu_id=4&web_menu_navdisplay=1&cate_id=0&dept_id=0&time_begin=&time_over=&limit=15&sort=0&field=x_title&content=&page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/div[2]/span/text()').extract_first()
        date = re.search(r"(\d{2}-\d{2}-\d{2})", date).groups()[0]
        date = '20' + date
        item['date'] = date

        title = response.xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/div[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="panel_body_content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
