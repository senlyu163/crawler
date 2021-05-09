# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
# from scrapy_splash import SplashRequest
#
# class A454Spider(CrawlSpider):
#     name = '454'
#     allowed_domains = ['linyou.gov.cn']
#     start_urls = [
#         'http://www.linyou.gov.cn/col/col1617/index.html',
#         'http://www.linyou.gov.cn/col/col3433/index.html',
#     ]
#
#     rules = (
#         Rule(LinkExtractor(restrict_xpaths='//div[@class="open"]/div/ul//li'), follow=True),
#         Rule(LinkExtractor(allow=r'/col/col\d+/index\.html'), follow=True),
#         # Rule(LinkExtractor(allow=r'/art/.*/art_\d+_\d+\.html'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'/col/.*&pageNum=\d+$'), follow=True),
#         Rule(LinkExtractor(allow=r'/col/.*&pageNum=\d+$'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#     def start_requests(self):
#         for su in self.start_urls:
#             yield SplashRequest(url=su)
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
#         print("$$$$$$$$$$$ ", response.url)
#         # item = ScrapySpiderItem()
#         # item['url'] = response.url
#         #
#         # date = response.xpath('//div[@class="small-title clearfix"]/span[1]').extract_first()
#         # date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#         # item['date'] = date
#         #
#         # title = response.xpath('//div[@class="con"]/p/text()').extract_first()
#         # item['title'] = title
#         #
#         # contents = response.xpath('//div[@class="main-txt"]').extract()
#         # item['contents'] = extract_CN_from_content(contents)
#         # return item
