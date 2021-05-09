# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A230Spider(CrawlSpider):
    name = '230'
    allowed_domains = ['rc.gov.cn']
    start_urls = [
        'http://www.rc.gov.cn/zwgk/default.htm',
        'http://www.rc.gov.cn/zwgk/tjxx/default.htm',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'[a-z]+/default\.htm$'), follow=True),
        Rule(LinkExtractor(allow=r'/[a-z]+/default\.htm$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="more"]'), follow=True),
        Rule(LinkExtractor(allow=r'[a-z]+/content_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'[a-z]+/[a-z]+/default\.htm'), follow=True),
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
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//div[@class="xl-date"]/span[1]').extract_first()
            date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//div[@class="main overflow"]/div[2]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="xl-content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="CBody"]/div[3]/div/div[1]/div[2]/ul/li[2]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="CBody"]/div[3]/div/div[1]/div[2]/ul/li[9]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="xl-content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
