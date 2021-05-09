# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A589Spider(CrawlSpider):
    name = '589'
    allowed_domains = ['xjnlk.gov.cn']
    # start_urls = ['http://www.xjnlk.gov.cn/index_zwgk/index_zwgk_qzqd.jsp?ainfolist5592t=10&ainfolist5592p=5&ainfolist5592c=25&urltype=tree.TreeTempUrl&wbtreeid=1079']
    start_urls = ['http://www.xjnlk.gov.cn/zwgk.htm']

    total_num = 0

    rules = (
        Rule(LinkExtractor(allow=r'zwgk/.*\.htm'), follow=True),
        Rule(LinkExtractor(allow=r'index_zwgk/.*\d+$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="ainfolist5544"]/div[1]/table//tr/td[2]/span'), callback='parse_item_1', follow=True),
        # Rule(LinkExtractor(allow=r'/info/egovinfo/.*\d+\.htm'), callback='parse_item_1', follow=True),
        Rule(LinkExtractor(allow=r'\?ainfolist5592t.*'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    # rules = (
    #     Rule(LinkExtractor(allow=r'zwgk/.*\.htm'), follow=True),
    #     Rule(LinkExtractor(allow=r'index_zwgk/.*\d+$'), follow=True),
    #     Rule(LinkExtractor(restrict_xpaths='//*[@id="ainfolist5732"]/div[1]/table//tr/td[2]'), callback='parse_item', follow=True),
    #     Rule(LinkExtractor(allow=r'/info/egovinfo/.*\d+\.htm'), callback='parse_item', follow=True),
    #     Rule(LinkExtractor(allow=r'\?ainfolist\d+t=\d+&ainfolist.*dpopenitem=[a-z]+$'), follow=True),
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    #
    # def _build_request(self, rule, link):
    #     r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 0.5})
    #     r.meta.update(rule=rule, link_text=link.text)
    #     return r
    #
    # def _requests_to_follow(self, response):
    #     # if not isinstance(response, HtmlResponse):
    #     #     return
    #     seen = set()
    #     for n, rule in enumerate(self._rules):
    #         links = [lnk for lnk in rule.link_extractor.extract_links(response)
    #                  if lnk not in seen]
    #         if links and rule.process_links:
    #             links = rule.process_links(links)
    #         for link in links:
    #             seen.add(link)
    #             r = self._build_request(n, link)
    #             yield rule.process_request(r)

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[3]/td/table/tr[2]/td/form/table/tr[2]/td/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[3]/td/table/tr[2]/td/form/table/tr[1]/td/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="vsb_newscontent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def parse_item_1(self, response):
        self.total_num = self.total_num + 1
        print("???????????????  ", response.url)
        print("total:  >>>>>>>>>>> ", self.total_num)
