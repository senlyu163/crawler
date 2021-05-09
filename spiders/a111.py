# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

from scrapy_splash import SplashRequest

class A111Spider(CrawlSpider):
    name = '111'
    allowed_domains = ['helong.gov.cn']
    start_urls = ['http://helong.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="page"]/div/div[2]/div/ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
    )

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 1, 'timeout': 90, 'images': 0, 'resource_timeout': 10})
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

        date = response.xpath('//*[@id="page"]/div/div[2]/div/div[1]/div[1]/span[1]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="listContent"]/h3/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="listContent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
