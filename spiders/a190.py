# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A190Spider(CrawlSpider):
    name = '190'
    allowed_domains = ['hnsc.gov.cn']
    start_urls = [
        'http://www.hnsc.gov.cn/html/zwgk/zfgkml/',
        'http://www.hnsc.gov.cn/html/zwgk/zfsydw/',
        'http://www.hnsc.gov.cn/html/zwgk/xzbsc/',
        # 'http://www.hnsc.gov.cn/html/zwgk/zfgkml/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/html/zwgk/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="list_right"]//ul/li[1]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/zwgk/[a-z]+/\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 1.5})
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

        date = response.xpath('//div[@class="detailed"]/div[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="detailed"]/div[1]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="zoom"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
