# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A379Spider(CrawlSpider):
    name = '379'
    allowed_domains = ['xd.km.gov.cn']
    start_urls = [
        'http://xd.km.gov.cn/zfxxgkml/ysqgk/',
        'http://xd.km.gov.cn/zfxxgkml/zzjg/',
        'http://xd.km.gov.cn/zfxxgkml/rsxx/',
        'http://xd.km.gov.cn/zfxxgkml/zfxxgkndbg/',
        'http://xd.km.gov.cn/zfxxgkml/zcjd/',
        'http://xd.km.gov.cn/zfxxgkml/zfwj/',
        'http://xd.km.gov.cn/zfxxgkml/zdgzxx/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/qljzrqd/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/phqgzxx/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/spypaqxx/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/hjbhxx/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/sbxx/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/jyxx/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/jycy/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/xzspxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/czsjxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/zfbzxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/gsdjhszshjgxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/ggzyjyxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/scaqsgxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/jghsfxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/jsjfxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/zdxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/gytdsfwzsbcxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/ylwsjgxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/kjglhxmjfxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/whjgxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/gyqyxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/lysczxhfwzlxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/mzxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/fpgzxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/cpzljgzfxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/zscqxzcfxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/gajgzdlyxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/gwyglxxgk/',
        'http://xd.km.gov.cn/zfxxgkml/zdlyxxgk/wsxwfbt/',
        'http://xd.km.gov.cn/zfxxgkml/czzjxx/',
        'http://xd.km.gov.cn/zfxxgkml/zfcg/',
        'http://xd.km.gov.cn/zfxxgkml/zdxmxx/',
        'http://xd.km.gov.cn/zfxxgkml/jhgh/',
        'http://xd.km.gov.cn/zfxxgkml/zfgzbg/',
        'http://xd.km.gov.cn/zfxxgkml/tjxx/',
        'http://xd.km.gov.cn/zfxxgkml/yjgl/',
        'http://xd.km.gov.cn/zfxxgkml/rdhy/',
        'http://xd.km.gov.cn/zfxxgkml/jytabljg/',
        'http://xd.km.gov.cn/zfxxgkml/zfgbdsj/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/c/\d+-\d+-\d+/\d+\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_d+\.shtml'), follow=True),
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
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//ul[@class="list"]/li[4]/span').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//li[@class="article-name"]/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="L2"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
