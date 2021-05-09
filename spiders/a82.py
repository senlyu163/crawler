# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re


class A82Spider(CrawlSpider):
    name = '82'
    allowed_domains = ['ningchengxian.gov.cn']
    start_urls = ['http://www.ningchengxian.gov.cn/zwgk/zwxxgk/zfxxgkml/']

    url_template = "http://www.ningchengxian.gov.cn/zwgk/zwxxgk/zfxxgkml/?pi={}"
    for n in range(30):
        url = url_template.format(n+1)
        start_urls.append(url)

    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="Navi_CategoryMapTree"]/ul'), follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="nav_zy"]/div[2]/ul[1]/li[2]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="xxgk_content"]/table//tr'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'openGov\d+\&pi=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print(response.url)
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url
            #
            date = response.xpath('//div[@id="article_Top"]/div/div[1]/table/tr/td[2]/text()').extract_first()
            date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('//div[@id="article_Top"]/div/h3/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="article_content_list"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url
            #
            date = response.xpath('//*[@id="article_Top"]/div/div[1]/table/tr/td[2]/text()').extract_first()
            date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="article_Top"]/div/h3/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//*[@id="fontzoom"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
