# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

from scrapy_splash import SplashRequest


class A160Spider(CrawlSpider):
    name = '160'
    allowed_domains = ['yongxin.gov.cn']
    start_urls = ['http://www.yongxin.gov.cn/html/class/xxgk/gggsy/index.html',
                  'http://www.yongxin.gov.cn/html/class/xwzx/xwdt/index.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="left_nav_url"]/li[2]/dt/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//ul[@class="menu_list_1"]//li/dt'), follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="dt_right"]/div[1]/div[2]/ul[1]//li'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        for su in self.start_urls:
            yield SplashRequest(url=su)


    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 0.5})
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def _requests_to_follow(self, response):
        # if not isinstance(response, HtmlResponse):
        #     return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def parse_item(self, response):

        print("$$$ ", response.url)

        # item = ScrapySpiderItem()
        # item['url'] = response.url
        #
        # date = response.xpath('//*[@id="leftbox"]/div/div[3]/text()[1]').extract_first()
        # date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        # item['date'] = date
        #
        # title = response.xpath('//div[@class="intr_title"]/text()').extract_first()
        # item['title'] = title
        #
        # contents = response.xpath('//div[@class="conTxt"]').extract()
        # item['contents'] = extract_CN_from_content(contents)
        # return item
