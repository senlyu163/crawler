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
# class A131Spider(CrawlSpider):
#     name = '131'
#     allowed_domains = ['yuexi.gov.cn']
#     start_urls = ['http://www.yuexi.gov.cn/index.php?m=content&c=index&a=lists&catid=504&id=1']
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/index\.php\?m=content&c=index&a=lists&catid=\d+&id=\d+'), follow=True),
#         Rule(LinkExtractor(allow=r'/xxgk/[a-z]+/\d+/\d+_\d+\.html'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=r'index\.php\?m=content&c=index&a=lists&catid=\d+&page=\d+&id=\d+'), follow=True),
#         # Rule(LinkExtractor(allow=r'/index\.php\?m=content&c=index&a=lists&catid=\d+&id=\d+'), follow=True),
#     )
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
#             date = response.xpath('/html/body/div[4]/div/div/div[2]/div/div[1]/table/tbody/tr[4]/td[4]/text()').extract_first()
#             date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#             item['date'] = date
#
#             title = response.xpath('/html/body/div[4]/div/div/div[2]/div/div[2]/h1/text()').extract_first()
#             item['title'] = title
#
#             contents = response.xpath('//div[@class="articleDetail"]').extract()
#             item['contents'] = extract_CN_from_content(contents)
#             return item
#         except:
#             print("there have format error.")
