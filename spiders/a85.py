# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A85Spider(CrawlSpider):
    name = '85'
    allowed_domains = ['houqi.gov.cn']
    start_urls = ['http://houqi.gov.cn/kzhq/zwgk/zwgk.shtml']

    rules = (
        Rule(LinkExtractor(allow=r'/kzhq/[a-zA-Z]+\d+/list\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/kzhq/[a-zA-Z]+/list\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/kzhq/[a-z]+/list\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/kzhq/gsgg/list\.shtml'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="ggnav"]//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list_\d+.shtml'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
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
        # print(response.url)
        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
        if ('qzqd' in response.url) or ('gsgg' in response.url) or ('xwfbh' in response.url) or ('hqxw' in response.url) or ('tzgg' in response.url):
            try:
                item = ScrapySpiderItem()
                item['url'] = response.url
                #
                date = response.xpath('/html/body/div[3]/div/div[2]/div[1]/text()').extract_first()
                date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
                item['date'] = date

                title = response.xpath('//div[@class="content"]/h1/text()').extract_first()
                item['title'] = title

                contents = response.xpath('//div[@class="zhengw"]').extract()
                item['contents'] = extract_CN_from_content(contents)
                return item
            except:
                print("there have no date in case 1.")
        else:
            try:
                item = ScrapySpiderItem()
                item['url'] = response.url
                #
                date = response.xpath('/html/body/div[3]/div/div[2]/div[1]/p[7]/em/text()').extract_first()
                date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
                item['date'] = date

                title = response.xpath('/html/body/div[3]/div/div[2]/div[1]/p[3]/em/text()').extract_first()
                item['title'] = title

                contents = response.xpath('//div[@class="zhengw"]').extract()
                item['contents'] = extract_CN_from_content(contents)
                return item
            except:
                print("there have no date in case 2.")
