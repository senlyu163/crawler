# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re
from scrapy_splash import SplashRequest

class A51CrawlSpider(CrawlSpider):
    name = '51_crawl'
    allowed_domains = ['heshun.gov.cn']
    start_urls = [
        'http://www.heshun.gov.cn/hsxxgk/xxgkml/ldjh'
    ]

    for i in range(10):
        temp_url = "http://www.heshun.gov.cn/zwgk/fdzdgknr2zfbgs/tzgg2zfbgs_{}".format(i + 1)
        start_urls.append(temp_url)

    for i in range(7):
        temp_url = "http://www.heshun.gov.cn/zwgk/fdzdgknr2zfbgs/zcjd2zfbgs_{}".format(i + 1)
        start_urls.append(temp_url)

    rules = (
        # Rule(LinkExtractor(allow=r'/hsxxgk/xxgkml/[a-z]+\d+$'), follow=True),
        # Rule(LinkExtractor(allow=r'/hsxxgk/xxgkml/[a-z]+$'), follow=True),
        # Rule(LinkExtractor(allow=r'/hsxxgk/xxgkml/[a-z]+/[a-z]+$'), follow=True),
        # Rule(LinkExtractor(allow=r'/hsxxgk/xxgkml/.*/content_\d+$'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="page"]'), follow=True),

        Rule(LinkExtractor(restrict_xpaths='//*[@id="xxgk-content"]/div[5]/div/div[2]/ul//li/a[1]'), callback='parse_item_one', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="xxgk-content"]/div[5]/div/div[2]/ul//li/a'), callback='parse_item_two', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    # def _build_request(self, rule, link):
    #     r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 2})
    #     r.meta.update(rule=rule, link_text=link.text)
    #     return r

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

    # def parse_item(self, response):
    #     item = ScrapySpiderItem()
    #     item['url'] = response.url

    #     date = response.xpath('/html/body/div[3]/div[1]/div[3]/center/div/div[1]').extract_first()
    #     date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
    #     item['date'] = date

    #     title = response.xpath('/html/body/div[3]/div[1]/div[3]/h2/text()').extract_first()
    #     item['title'] = title

    #     contents = response.xpath('//div[@class="article_content"]').extract()
    #     item['contents'] = extract_CN_from_content(contents)
    #     return item

    # def parse_item_two(self, response):
    def parse_item_one(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="xxgk-content"]/div[5]/article/div[1]/div[1]/table/tbody/tr[2]/td[2]/text()').extract_first()
        try:
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        except ...:
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]

        item['date'] = date

        title = response.xpath('//*[@id="xxgk-content"]/div[5]/article/div[1]/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="xxgk-content"]/div[5]/article/div[1]/div[3]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    # def parse_item_one(self, response):
    def parse_item_two(self, response):

        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[6]/div[1]/div[2]/div[1]/text()').extract_first()
        try:
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        except ...:
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        # date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[6]/div[1]/div[2]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/div[6]/div[1]/div[2]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
