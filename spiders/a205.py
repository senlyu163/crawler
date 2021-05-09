# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
#
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
#
# from scrapy_splash import SplashRequest
#
# class A205Spider(CrawlSpider):
#     name = '205'
#     allowed_domains = ['djk.gov.cn']
#     start_urls = [
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/zcfg/zcjd/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/zcfg/zfwj/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/zcfg/zfbwj/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/fzgh/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/sjtj/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/czzj/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/aqsc/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/hjbh/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/zdcq/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/zbcg/zbgg/list_3978.shtm',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/bzxzf/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/spypaq/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/jgsf/list_3978.shtml',
#         'http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/xzgcgk/list_3978.shtml',
#     ]
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/rsxx/rsrm/\d+/t\d+_\d+\.shtml'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'list_\d+_\d+\.shtml'), follow=True),
#         Rule(LinkExtractor(allow=r'/d+/td+_d+\.shtml'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'/xxgkml/[a-z]+/[a-z]+/$'), follow=True),
#         Rule(LinkExtractor(allow=r'/xxgkml/[a-z]+/$'), follow=True),
#         Rule(LinkExtractor(allow=r'/zcqgh/201811/t20181121_1614784.shtml'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#     def start_requests(self):
#         for url in self.start_urls:
#             # Splash 默认是render.html,返回javascript呈现页面的HTML。
#             yield SplashRequest(url, args={'wait': 1})
#
#     def _build_request(self, rule, link):
#         r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 0.5})
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
#         try:
#             item = ScrapySpiderItem()
#             item['url'] = response.url
#
#             date = response.xpath('/html/body/div[3]/div[1]/div/table/tr[1]/td[3]/text()').extract_first()
#             date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
#             item['date'] = date
#
#             title = response.xpath('/html/body/div[3]/div[2]/h1/text()').extract_first()
#             item['title'] = title
#
#             contents = response.xpath('//div[@class="xxgkxq-cont"]').extract()
#             item['contents'] = extract_CN_from_content(contents)
#             return item
#         except:
#             item = ScrapySpiderItem()
#             item['url'] = response.url
#
#             date = response.xpath('//div[@class="field_con"]/table[1]/tr[1]/td[3]/text()').extract_first()
#             date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
#             item['date'] = date
#
#             title = response.xpath('/html/body/div[3]/div[2]/h1/text()').extract_first()
#             item['title'] = title
#
#             contents = response.xpath('//div[@class="xxgkxq-cont"]').extract()
#             item['contents'] = extract_CN_from_content(contents)
#             return item
#
