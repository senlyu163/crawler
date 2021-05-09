# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A455Spider(CrawlSpider):
    name = '455'
    allowed_domains = ['sxtb.gov.cn']
    start_urls = [
        'http://www.sxtb.gov.cn/info/iList.jsp?cat_id=10508',
        'http://www.sxtb.gov.cn/info/iList.jsp?cat_id=10021',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/jczwgk/.*/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/info/iList\.jsp\?cat_id=\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'\?cat_id=\d+&cur_page=\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/zdzl/.*/\d+.htm'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[8]/div[4]/div/div[2]/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[8]/div[4]/div/div[1]/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="m-ct-artcle"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
