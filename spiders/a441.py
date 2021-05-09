# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A441Spider(CrawlSpider):
    name = '441'
    allowed_domains = ['heqing.gov.cn']
    start_urls = [
        'http://www.heqing.gov.cn/dlzhqx/c102096/common_list.shtml',
        'http://www.heqing.gov.cn/dlzhqx/c102105/common_list.shtml',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/dlzhqx/c\d+/common_list\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/dlzhqx/c\d+/\d+/.*\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'common_list_\d+\.shtml'), follow=True),
        Rule(LinkExtractor(allow=r'/dlzhqx/c\d+/jump\.shtml'), follow=True),
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

            date = response.xpath('/html/body/div[3]/div[2]/div[2]/ul/li[2]').extract_first()
            date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[3]/div[2]/h1/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@id="NewsContent"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[3]/div[2]/div[1]/ul/li[2]').extract_first()
            date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[3]/div[2]/h1/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@id="NewsContent"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
