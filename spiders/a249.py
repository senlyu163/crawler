# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A249Spider(CrawlSpider):
    name = '249'
    allowed_domains = ['glls.gov.cn']
    start_urls = [
        'http://www.glls.gov.cn/zwgk/',
        'http://www.glls.gov.cn/zwgk/jcxxgk/gfxwj/xzfwj/lzf/',
        'http://www.glls.gov.cn/zwgk/jcxxgk/gfxwj/xzfwj/lzbf/',
        'http://www.glls.gov.cn/zwgk/jcxxgk/gfxwj/bmwj/fzhggj/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/zdly/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),

        Rule(LinkExtractor(allow=r'/[a-z]+/$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[7]/div[2]/div/div[1]/p/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[7]/div[2]/div/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="articlenr"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
