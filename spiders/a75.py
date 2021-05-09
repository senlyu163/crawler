# # -*- coding: utf-8 -*-
# import scrapy
#
# from scrapy_splash import SplashRequest
# import requests
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
#
# class A75Spider(scrapy.Spider):
#     name = '75'
#     allowed_domains = ['wuchuan.gov.cn']
#     start_urls = ['http://www.wuchuan.gov.cn/zwgk/jgsz/']
#
#     def parse(self, response):
#         navi_list = response.xpath('//div[@class="TylieB-left l"]//li//a/@href').extract()
#         # have 2 grade menu.
#         # czgk, zfwj, yfxz,
#         not_sub_menu = []
#         not_sub_menu.append(navi_list[4])
#         not_sub_menu.append(navi_list[6])
#         not_sub_menu.append(navi_list[8])
#         not_sub_menu.append(navi_list[10])
#         not_sub_menu.append(navi_list[14])
#         # print(not_sub_menu)
#         sub_menu = []
#         sub_menu.append(navi_list[12])
#         sub_menu.append(navi_list[16])
#         sub_menu.append(navi_list[22])
#         # print(sub_menu)
#         for nsm in not_sub_menu:
#             complete_url_nsm = response.urljoin(nsm)
#             yield SplashRequest(url=complete_url_nsm, callback=self.extract_table_url, args={"wait": 0.5})
#
#         for sm in sub_menu:
#             complete_url_sm = response.urljoin(sm)
#             yield scrapy.Request(url=complete_url_sm, callback=self.extract_sub_menu)
#
#     def extract_table_url(self, response):
#         table_url = response.xpath('//div[@class="TylieB-right r"]/ul[1]//li//a/@href').extract()
#         # print(table_url)
#         for tu in table_url:
#             complete_url = response.urljoin(tu)
#             yield scrapy.Request(url=complete_url, callback=self.extract_context)
#
#         # next page
#         for i in range(100):
#             # index_num = "index_{}"
#             next_url = response.urljoin("index_{}.html".format(i+1))
#             # print("^^^^^", next_url)
#             if requests.get(url=next_url).status_code == int('200'):
#                 yield scrapy.Request(url=next_url, callback=self.extract_table_url)
#             else:
#                 break
#
#
#     def extract_sub_menu(self, response):
#         sub_list = response.xpath('//div[@class="TylieB-left l"]//li//a/@href').extract()
#         for sl in sub_list:
#             complete_url = response.urljoin(sl)
#             yield scrapy.Request(url=complete_url, callback=self.extract_table_url)
#
#     def extract_context(self, response):
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('//table[@class="xxgk_info"]/tr[2]/td[3]/text()').extract_first()
#         date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('//table[@class="xxgk_info"]/tr[1]/td[1]/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@id="para"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item