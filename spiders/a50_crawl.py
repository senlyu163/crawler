# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re
from scrapy_splash import SplashRequest


class A50CrawlSpider(CrawlSpider):
    name = '50_crawl'
    allowed_domains = ['jzzq.gov.cn']
    # start_urls = ['http://www.jzzq.gov.cn/publicity/zfwj']
    start_urls = ['http://www.jzzq.gov.cn/zwgkzy/fdzdgknr']

    rules = (
        # Rule(LinkExtractor(allow=r'/zwgkzy/[a-z]+_\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="xxgk-content"]/div[5]/div/div[2]/ul//li/a[2]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/publicity/[a-z]+/[a-z]+\?keyword=\d+$'), follow=True),
        # Rule(LinkExtractor(allow=r'/publicity/[a-z]+/[a-z]+/\d+$'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/publicity/[a-z]+_\d+$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    for i in range(142):
        temp_url = "http://www.jzzq.gov.cn/zwgkzy/fdzdgknr_{}".format(i + 1)
        start_urls.append(temp_url)



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

        # print("@@@@@@@@@@@@@@@", response.url)
        item = ScrapySpiderItem()
        item['url'] = response.url

        # date = response.xpath('//*[@id="content"]/div/table/tbody/tr[2]/td[2]').extract_first()
        date = response.xpath('//*[@id="xxgk-content"]/div[5]/article/div[1]/div[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        # title = response.xpath('//*[@id="content"]/div/div[1]/h3/text()').extract_first()
        title = response.xpath('//*[@id="xxgk-content"]/div[5]/article/div[1]/h2/text()').extract_first()
        item['title'] = title

        # contents = response.xpath('//div[@class="govDetailContent"]').extract()
        contents = response.xpath('//*[@id="xxgk-content"]/div[5]/article').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
