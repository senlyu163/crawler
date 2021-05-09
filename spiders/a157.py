# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

from scrapy_splash import SplashRequest

class A157Spider(CrawlSpider):
    name = '157'
    allowed_domains = ['jianxian.gov.cn']
    start_urls = ['http://jianxian.gov.cn/',
                  'http://www.jianxian.gov.cn/html/zwyw/index.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="708842639722"]/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="708842639722"]/ul/font/font//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="188350616197"]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="list_rightrl"]//li/span[2]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 2})
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
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[4]/div[2]/p[3]/text()').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[4]/div[2]/p[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="ziticonteng"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
