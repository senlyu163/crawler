# # -*- coding: utf-8 -*-
# import scrapy
#
#
# class A48Spider(scrapy.Spider):
#     name = '48'
#     allowed_domains = ['wuxiang.gov.cn']
#     start_urls = ['http://www.wuxiang.gov.cn/wxxxgk/zfxxgk/zfxxgkml/wjgk/']
#
#     def parse(self, response):
#         navi_list_1 = response.xpath('/html/body/div/ul/li[5]/ul/li/ul//li/a[2]/@href').extract()
#         navi_list_2 = response.xpath('/html/body/div/ul/li[5]/ul/li/ul//li/dl//dd/a/@href').extract()
#         navi_list = []
#         for nl_1 in navi_list_1:
#             navi_list.append(nl_1)
#         for nl_2 in navi_list_2:
#             navi_list.append(nl_2)
#
#         for nl in navi_list:
#             url = response.urljoin(nl)
#             print("@@@@@@@@@@@@@@  ", url)
#             # yield scrapy.Request(url=url, callback=self.extract_iframe)
#
#     def extract_iframe(self, response):
#         iframe_item = response.xpath('//iframe/@src').extract_first()
#         url = response.urljoin(iframe_item)
#         print("#############  ", url)
#         # yield scrapy.Request(url=url, callback=self.extract_table_urls)
#
#     def extract_table_urls(self, response):
#         url_list = response.xpath('//ul[@class="list-li"]').extract()
#         print("@@@@@@@@@@@@@@  ", url_list)
