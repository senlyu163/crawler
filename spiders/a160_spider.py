# # -*- coding: utf-8 -*-
# import scrapy
#
# from scrapy_splash import SplashRequest
#
# class A160SpiderSpider(scrapy.Spider):
#     name = '160_spider'
#     allowed_domains = ['yongxin.gov.cn']
#     start_urls = ['http://www.yongxin.gov.cn/html/class/xxgk/gggsy/index.html']
#
#     def parse(self, response):
#         yield SplashRequest(url=response.url, callback=self.prt_url, args={"wait": 0.5})
#
#     def prt_url(self, response):
#         urls = response.xpath('//*[@id="left_nav_url"]/li[2]/dt/a/@href').extract()
#         for u in urls:
#             print("##$$$$ ", u)
