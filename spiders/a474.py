# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A474Spider(CrawlSpider):
    name = '474'
    allowed_domains = ['liuba.gov.cn']
    start_urls = [
        'http://www.liuba.gov.cn/xxgk/',
        'http://www.liuba.gov.cn/xxgk/xxgkml/zdlyxxgk/',
        'http://www.liuba.gov.cn/xxgk/xxgkml/zfgzbg/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/zwdt/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
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

            date = response.xpath('/html/body/div/div[1]/div[3]/div/table[1]/tr[4]/td[2]/p').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div/div[1]/div[3]/div/table[3]/tr/td/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/div/div[1]/div[3]/div/table[4]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div/div[1]/div[3]/div/table[1]/tbody/tr[4]/td[2]/p').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div/div[1]/div[3]/div/table[3]/tbody/tr/td/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/div/div[1]/div[3]/div/table[4]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
