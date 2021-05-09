# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A478Spider(CrawlSpider):
    name = '478'
    allowed_domains = ['sxsd.gov.cn']
    start_urls = ['http://www.sxsd.gov.cn/html/zwgk/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/html/zwgk/xzfxxgkml/[a-z]+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/zwgk/xzfxxgkml/[a-z]+/[a-z]+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/zwgk/xzfxxgkml/[a-z]+/[a-z]+/\d+/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk_list\.rt\?channlCid=\d+&channlId=\d+&pageNo=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/news_list\.rt\?channlCid=\d+&channlId=\d+&pageNo=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    # def _build_request(self, rule, link):
    #     #     r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 0.5})
    #     #     r.meta.update(rule=rule, link_text=link.text)
    #     #     return r
    #     #
    #     # def _requests_to_follow(self, response):
    #     #     # if not isinstance(response, HtmlResponse):
    #     #     #     return
    #     #     seen = set()
    #     #     for n, rule in enumerate(self._rules):
    #     #         links = [lnk for lnk in rule.link_extractor.extract_links(response)
    #     #                  if lnk not in seen]
    #     #         if links and rule.process_links:
    #     #             links = rule.process_links(links)
    #     #         for link in links:
    #     #             seen.add(link)
    #     #             r = self._build_request(n, link)
    #     #             yield rule.process_request(r)

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="xwbtsj"]/div/table/tbody/tr[3]/td[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="xwbtsj"]/div/div[2]/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
