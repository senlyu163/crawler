# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
#
# from ..utils import extract_CN_from_content
# from ..items import ScrapySpiderItem
# import re
# from scrapy_splash import SplashRequest
#
# class A199Spider(CrawlSpider):
#     name = '199'
#     allowed_domains = ['yx.gov.cn']
#     start_urls = ['http://www.yx.gov.cn/zwgk/']
#
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/zfxxgkml/[a-z]+/\?CHANNELID=\d+'), follow=True),
#         Rule(LinkExtractor(allow=r'/zfxxgkml/[a-z]+/[a-z]+/\?CHANNELID=\d+'), follow=True),
#         Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
#         Rule(LinkExtractor(allow=r'/zwgk/[a-z]+/[a-z]+/$'), follow=True),
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
#         # if not isinstance(response, (SplashTextResponse, SplashJsonResponse, SplashResponse, HtmlResponse)):
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
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/p[2]/span[2]/text()').extract_first()
#         date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/p[1]/span/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@class="article_main"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item
