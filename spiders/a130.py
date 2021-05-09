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
# class A130Spider(CrawlSpider):
#     name = '130'
#     allowed_domains = ['susong.gov.cn']
#     start_urls = ['http://www.susong.gov.cn/public/User/PageInfo2.aspx?unitId=59&clsid=0']
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/public/User/PageInfo\d+\.aspx\?unitId=\d+&clsid=\d+'), follow=True),
#         Rule(LinkExtractor(allow=r'/public/User/DisplayInfo\d+\.aspx\?ItemId=\d+&unitId=\d+'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(restrict_xpaths='div[@class="Pages"]'), follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
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
#             date = response.xpath('//*[@id="container"]/div/div[2]/table/tbody/tr[3]/td[4]/text()').extract_first()
#             date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#             item['date'] = date
#
#             title = response.xpath('//*[@id="container"]/div/div[2]/table/tbody/tr[6]/td[2]/text()').extract_first()
#             item['title'] = title
#
#             contents = response.xpath('//div[@class="is-content-detail"]').extract()
#             item['contents'] = extract_CN_from_content(contents)
#             return item
#         except:
#             print("there have format error.")
