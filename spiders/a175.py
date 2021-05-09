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
#
# class A175Spider(CrawlSpider):
#     name = '175'
#     allowed_domains = ['hnhx.gov.cn']
#     start_urls = ['http://www.hnhx.gov.cn/xxgk.htm']
#
#     url_template = "http://www.hnhx.gov.cn/xxgk-ssjgy.jsp?ainfolist112372t=1106&ainfolist112372p={}&ainfolist112372c=10&gitcatcode=&fgidate=&lgidate=&wbtreeid=1078&giindentifier=&giscatcode=+&urltype=egovinfo.EgovSearchList&gicategorycode=&stype=advance&giccode=&gipubcode=+&gititle=&gidocno="
#     for n in range(1106):
#         url = url_template.format(n+1)
#         start_urls.append(url)
#
#     rules = (
#         Rule(LinkExtractor(restrict_xpaths='//*[@id="ainfolist112372"]/div[1]/table/tbody/table//tr/td[2]/span'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(restrict_xpaths='//*[@id="ainfolist112372"]/div[1]/table//tr/td[2]/span'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'/info/\d+/\d+\.htm'), callback='parse_item', follow=True),
#         # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#     def start_requests(self):
#         for su in self.start_urls:
#             yield SplashRequest(url=su, args={"wait": 2})
#
#     def _build_request(self, rule, link):
#         r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 2})
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
#             date = response.xpath('//td[@style="background-color: #fffcf6;border: 1px solid #edc77b;padding-top: 3px;padding-right: 4px;padding-left: 4px;vertical-align: top;height: 60px"]/table/tr/td[6]/text()').extract_first()
#             date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
#             item['date'] = date
#
#             title = response.xpath('//td[@style="TEXT-ALIGN: center;LINE-HEIGHT: 200%;FONT-FAMILY: 宋体;HEIGHT: 26px;COLOR: #222222;FONT-SIZE: 14pt;FONT-WEIGHT: bold"]/text()').extract_first()
#             item['title'] = title
#
#             contents = response.xpath('//div[@id="egovinfocontenttable"]').extract()
#             item['contents'] = extract_CN_from_content(contents)
#             return item
#         except:
#             item = ScrapySpiderItem()
#             item['url'] = response.url
#
#             date = response.xpath('//span[@class="timestyle112078"]/text()').extract_first()
#             date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#             item['date'] = date
#
#             title = response.xpath('//td[@class="titlestyle112078"]/text()').extract_first()
#             item['title'] = title
#
#             contents = response.xpath('//*[@id="vsb_content_500"]').extract()
#             item['contents'] = extract_CN_from_content(contents)
#             return item
