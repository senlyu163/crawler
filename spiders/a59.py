# # -*- coding: utf-8 -*-
# import scrapy
#
# from scrapy_splash import SplashRequest
#
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
#
# class A59Spider(scrapy.Spider):
#     name = '59'
#     allowed_domains = ['wzx.sxxz.gov.cn']
#     start_urls = ['http://wzx.sxxz.gov.cn/wzxzw/zwgk/xxgkzn/']
#
#     def parse(self, response):
#         # gkgd = response.xpath("/html/body/div[2]/div/div[1]/ul/li[2]/a/@href").extract_first()
#         # main_domain = 'http://wzx.sxxz.gov.cn/wzxzw/zwgk/'
#         # complete_url = main_domain + gkgd[-8:]
#         # yield SplashRequest(url=complete_url, callback=self.gkgd, args={"wait": 0.5})
#
#         direct_url = []
#         loop_url = []
#         navi_list = response.xpath('//ul[@class="item-nav"]//a/@href').extract()
#         for nl in navi_list[1:]:
#             navi_url = response.urljoin(nl)
#             if 'xxgkgd' in navi_url:
#                 direct_url.append(navi_url)
#             elif 'xxgknb' in navi_url:
#                 direct_url.append(navi_url)
#
#             elif 'jgsz' in navi_url: # this class have sub web.
#                 # yield scrapy.Request(url=navi_url, callback=self.extract_jgsz)
#                 continue
#             # if 'szfwj' in navi_url: # this class is all pdf format.
#             #     pass
#             else:
#                 loop_url.append(navi_url)
#         print(direct_url, "$$$", loop_url)
#
#         for du in direct_url:
#             yield scrapy.Request(url=du, callback=self.extract_table_url)
#
#         for lu in loop_url:
#             yield SplashRequest(url=lu, callback=self.extract_table_url, args={"wait": 0.5})
#             # next page
#             pages_text = response.xpath('//*[@id="searchsection"]/div[2]/text()[1]').extract_first()
#             page_num = re.search(r"/(\d+)页", pages_text).groups()[0]
#             for n in page_num:
#                 n = n + 1
#                 next_url = lu + 'index_' + n
#                 yield SplashRequest(url=next_url, callback=self.extract_table_url, args={"wait": 0.5})
#
#     def extract_table_url(self, response):
#         table_rl = response.xpath('//div[@id="searchsection"]/ul//li/a/@href').extract()
#         for tr in table_rl:
#             # complete_url = response.url + tr[2:]
#             complete_url = response.urljoin(tr)
#             yield scrapy.Request(url=complete_url, callback=self.extract_con)
#             # print("*******", complete_url)
#
#         # next page
#         # pages_text = response.xpath('//*[@id="searchsection"]/div[2]/text()[1]').extract_first()
#         # page_num = re.search(r"(/\d+页)", pages_text).groups()[0]
#
#
#     def extract_con(self, response):
#         if '.zip' in response.url:
#             pass
#         else:
#             try:
#                 item = ScrapySpiderItem()
#                 item['url'] = response.url
#
#                 title = response.xpath('/html/body/div[2]/div[1]/div/div[1]/h2/text()').extract_first()
#                 item['title'] = title
#
#                 # date = response.xpath('/html/body/div[2]/div[1]/div/div[1]/p/text()[1]').extract_first()
#                 # date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#                 # item['date'] = date
#
#                 date = response.xpath('/html/body/div[2]/div[1]/div/div[1]/p/text()[1]').extract_first()
#                 date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#                 item['date'] = date
#
#                 contents = response.xpath('/html/body/div[2]/div[1]').extract()
#                 item['contents'] = extract_CN_from_content(contents)
#                 yield item
#             except:
#                 print("error.")
