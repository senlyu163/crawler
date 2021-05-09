# # -*- coding: utf-8 -*-
# import scrapy
#
# from scrapy_splash import SplashRequest
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
#
#
# class A82Spider(scrapy.Spider):
#     name = '82_backup'
#     allowed_domains = ['ningchengxian.gov.cn']
#     start_urls = ['http://www.ningchengxian.gov.cn/zwgk/zwxxgk/zfxxgkml/']
#
#     def parse(self, response):
#         url_list = response.xpath('//*[@id="ctl00_Navi_SecondLevelNavi_148964881976820_Navi_CategoryMapTree_14916189503041"]/li/ul//li/span/a/@href').extract()
#         for ul in url_list:
#             complete_url = response.urljoin(ul)
#             yield scrapy.Request(url=complete_url, callback=self.extract_table)
#
#     def extract_table(self, response):
#         # get max next page num
#         con = response.xpath('//*[@id="we7layout_148964878486524"]/div[2]/div/div/div[4]/div/a[7]/@href').extract_first()
#         max_num = re.search(r"pi=(\d+)", con).groups()[0]
#         for i in range(max_num):
#             complete_url = response.url + "&pi={}".format(i+1)
#             yield scrapy.Request(url=complete_url, callback=self.extract_table_url)
#
#     def extract_table_url(self, response):
#         table_list = response.xpath(
#             '//*[@id="we7layout_148964878486524"]/div[2]/div/div/div[3]/table/tbody//tr/td[2]/a').extract()
#         for tl in table_list:
#             complete_url = response.urljoin(tl)
#             yield scrapy.Request(url=complete_url, callback=self.extract_context)
#
#     def extract_context(self, response):
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('//*[@id="article_Top"]/div/div[1]/table/tbody/tr/td[2]/text()').extract_first()
#         date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('//*[@id="article_Top"]/div/h3/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@class="article_content_list"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item
