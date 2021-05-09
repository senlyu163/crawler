# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

import requests

class A327Spider(CrawlSpider):
    name = '327'
    allowed_domains = ['liuzhi.gov.cn']
    start_urls = [
        'http://www.liuzhi.gov.cn/zwgk/xxgkml/zdlyxx/qlqdhzrqd/qlqd/'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/zwgk/xxgkml/zdlyxx/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/xxgkml/[a-z]+/[a-z]+/$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/xxgkml/[a-z]+/[a-z]+/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/zwgk/xxgkml/[a-z]+/[a-z]+/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )
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
        for i in range(100):
            complete_url = response.urljoin('list_{}.html'.format(i+1))
            if requests.get(url=complete_url).status_code == int('200'):
                yield SplashRequest(url=complete_url, callback=self.extract_table, args={"wait": 0.5})
            else:
                break
        # item = ScrapySpiderItem()
        # item['url'] = response.url
        #
        # date = response.xpath('//*[@id="c"]/div[4]/span[1]').extract_first()
        # date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        # item['date'] = date
        #
        # title = response.xpath('//*[@id="c"]/div[2]/text()').extract_first()
        # item['title'] = title
        #
        # contents = response.xpath('//*[@id="Zoom"]').extract()
        # item['contents'] = extract_CN_from_content(contents)
        # return item

    def extract_table(self, response):
        url_list = response.xpath('//*[@id="data"]//tr/td[1]/h1/a/@href').extract()
        for ul in url_list:
            yield scrapy.Request(url=ul, callback=self.extract_context)

    def extract_context(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="c"]/div[4]/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="c"]/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="Zoom"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
