# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A475Spider(CrawlSpider):
    name = '475'
    allowed_domains = ['foping.gov.cn']
    start_urls = ['http://www.foping.gov.cn/xxgk/xxgkml/list.html']

    url_template = "http://www.foping.gov.cn/xxgk/xxgkml/list_{}.html"
    for n in range(49):
        url = url_template.format(n+1)
        start_urls.append(url)

    rules = (
        # Rule(LinkExtractor(allow=r'/[a-z]+/list\.html'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="tcon"]//ul/li[3]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'list_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div/div/div/div[2]/div[3]/div[1]/table/tr[3]/td[4]').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div/div/div/div[2]/div[3]/h6/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/div/div/div/div[2]/div[3]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div/div/div/div[1]/div[3]/div[1]/table/tr[4]/td[2]').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div/div/div/div[1]/div[3]/h6/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/div/div/div/div[1]/div[3]/div[3]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
