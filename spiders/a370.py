# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
#
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
# import time
# import requests
#
# from scrapy_splash import SplashRequest
#
# class A370Spider(CrawlSpider):
#     name = '370'
#     allowed_domains = ['qdndz.gov.cn']
#     start_urls = ['http://www.qdndz.gov.cn/xxgk/xxgkml/jcgk/zcwj/xzfwj/index.html']
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/xxgk/xxgkml/[a-z]+/[a-z]+/$'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'/xxgk/xxgkml/[a-z]+/[a-z]+/[a-z]+/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(restrict_xpaths='//*[@id="data"]//tr/td[1]/h1'), follow=True),
#         # Rule(LinkExtractor(allow=r'list_\d+\.html'), follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#     def _build_request(self, rule, link):
#         r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 1.5})
#         r.meta.update(rule=rule, link_text=link.text)
#         return r
#
#     def _requests_to_follow(self, response):
#         # if not isinstance(response, HtmlResponse):
#         #     return
#         seen = set()
#         for n, rule in enumerate(self._rules):
#             links = [lnk for lnk in rule.link_extractor.extract_links(response)
#                      if lnk not in seen]
#             if links and rule.process_links:
#                 links = rule.process_links(links)
#             for link in links:
#                 seen.add(link)
#                 r = self._build_request(n, link)
#                 yield rule.process_request(r)
#
#     def parse_item(self, response):
#         yield scrapy.Request(url=response.url, callback=self.extract_table_url)
#         for i in range(1000):
#             time.sleep(1)
#             complete_url = response.url + "list_{}.html".format(i+1)
#             if requests.get(url=complete_url).status_code == int('200'):
#                 yield scrapy.Request(url=complete_url, callback=self.extract_table_url)
#             else:
#                 break
#
#         # item = ScrapySpiderItem()
#         # item['url'] = response.url
#         #
#         # date = response.xpath('//div[@class="title"]/div[1]').extract_first()
#         # date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
#         # item['date'] = date
#         #
#         # title = response.xpath('//div[@class="title"]/h1/text()').extract_first()
#         # item['title'] = title
#         #
#         # contents = response.xpath('//div[@class="content2"]').extract()
#         # item['contents'] = extract_CN_from_content(contents)
#         # return item
#
#     def extract_table_url(self, response):
#         table_url = response.xpath('//*[@id="data"]//tr/td[1]/h1/a/@href').extract()
#         for tu in table_url:
#             time.sleep(1)
#             yield scrapy.Request(url=tu, callback=self.extract_context)
#
#     def extract_context(self, response):
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('//div[@class="title"]/div[1]').extract_first()
#         date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('//div[@class="title"]/h1/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@class="content2"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item
