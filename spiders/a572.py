# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
#
# class A572Spider(CrawlSpider):
#     name = '572'
#     allowed_domains = ['xjwqx.gov.cn']
#     start_urls = ['http://xjwqx.gov.cn/']
#
#     rules = (
#         # Rule(LinkExtractor(allow=r'/info/.*id=\d+'), follow=True),
#         # Rule(LinkExtractor(allow=r'/P/C/\d+\.htm'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'\?node_id=GKfpb&site_id=CMSwqx&cat_id=\d+&cur_page=\d+'), follow=True),
#         Rule(LinkExtractor(restrict_xpaths='//div[@class="am-u-lg-9"]/iframe/@src'), callback='parse_item_iframe', follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#     def parse_item(self, response):
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('//*[@id="gk-info"]/tr[4]/td[4]').extract_first()
#         date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('//*[@id="gk-info"]/tr[2]/td[2]/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@id="text"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item
#
#     def parse_item_iframe(self, response):
#         print(">>>>>>>>>>>>>>>>>>>>  ", response.url)
