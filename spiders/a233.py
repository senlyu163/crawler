# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
#
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
# from scrapy_splash import SplashRequest
#
# class A233Spider(CrawlSpider):
#     name = '233'
#     allowed_domains = ['jh.gov.cn']
#     start_urls = ['http://www.jh.gov.cn/jh/xhtml/zwgkml.html',
#                   'http://www.jh.gov.cn/jhjyj/0200/jhzwgk_right.shtml']
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/[a-z]+/[a-z]+/[a-z]+List\.shtml'), follow=True),
#         Rule(LinkExtractor(allow=r'/[a-z]+/\d+/\d+/.*\.shtml'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'jhzwgk_right_2.shtml'), follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#
#     def parse_item(self, response):
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('/html/body/div[4]/div/div/div[2]/table/tr[2]/td[4]/publishtime').extract_first()
#         date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('/html/body/div[4]/div/div/div[2]/table/tr[3]/td[2]/ucaptitle/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@id="zoomcon"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item
