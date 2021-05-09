# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A425Spider(CrawlSpider):
    name = '425'
    allowed_domains = ['yanshan.gov.cn']
    start_urls = ['http://www.yanshan.gov.cn/publicity']

    rules = (
        Rule(LinkExtractor(allow=r'/publicity/[a-z]+/\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zdlyxx/[a-z]+/content_\d+'), callback='parse_item_2', follow=True),
        Rule(LinkExtractor(allow=r'/publicity_\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/zdlyxx/[a-z]+$'), follow=True),
        Rule(LinkExtractor(allow=r'/zdlyxx/[a-z]+_\d+$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    # def _build_request(self, rule, link):
    #     r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 2})
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

        date = response.xpath('//*[@id="content"]/div/table/tbody/tr[2]/td[2]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//h3[@class="title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="govIntro"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def parse_item_2(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="content"]/article/div[1]/div[1]/span[2]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//h2[@class="title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="conTxt"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
