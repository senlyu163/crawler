# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
#
#
# class A122Spider(CrawlSpider):
#     name = '122'
#     allowed_domains = ['hd.huachuan.gov.cn']
#     start_urls = ['http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?wj=1'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?wj=2'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?wj=3'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?wj=4'
#
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=1'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=2'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=3'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=4'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=5'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=6'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=7'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=8'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=9'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=10'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=11'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=12'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=13'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=14'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=15'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=16'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=17'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?zt=18'
#
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?bm=1'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?bm=2'
#
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?tc=1'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?tc=2'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?tc=3'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?tc=4'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?tc=5'
#                   , 'http://hd.huachuan.gov.cn/aspx/gkml_list.aspx?tc=6']
#
#     rules = (
#         Rule(LinkExtractor(restrict_xpaths='//div[@class="rinr"]/table[1]//tr/td[2]'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#     def parse_item(self, response):
#         item = {}
#         #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
#         #item['name'] = response.xpath('//div[@id="name"]').get()
#         #item['description'] = response.xpath('//div[@id="description"]').get()
#         return item
