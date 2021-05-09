# # -*- coding: utf-8 -*-
# import scrapy
#
# import re
#
# class A55Spider(scrapy.Spider):
#     name = '55'
#     allowed_domains = ['fsx.sxxz.gov.cn']
#     start_urls = ['http://fsx.sxxz.gov.cn/fsxzw/zwgk/xxgkzn/']
#
#     def parse(self, response):
#         navi_list = response.xpath('//ul[@class="item-nav"]//@href').extract()
#         web_domain = "http://fsx.sxxz.gov.cn/fsxzw/zwgk"
#         for navi in navi_list:
#             complete_url = web_domain + navi[2:]
#             yield scrapy.Request(url=complete_url, callback=self.extract_table)
#
#     def extract_table(self, response):
#         web_url = response.url
#         url_rule = re.compile(r'/\d+/t\d+_\d+\.html$')
#         if url_rule.match(web_url):
#             yield scrapy.Request(url=web_url, callback=self.table_url)
