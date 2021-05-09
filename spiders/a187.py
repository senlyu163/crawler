# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A187Spider(CrawlSpider):
    name = '187'
    allowed_domains = ['yucheng.gov.cn']
    start_urls = [
        'http://www.yucheng.gov.cn/html/zhengfu/wenjian.html',
        'http://www.yucheng.gov.cn/html/jiceng/jiceng.html',
        'http://www.yucheng.gov.cn/html/zhengfu/dating.html',
        'http://www.yucheng.gov.cn/html/meiti/meiti.html',
        'http://www.yucheng.gov.cn/html/tongzhi/tongzhi.html',
        'http://www.yucheng.gov.cn/html/sjzxzjc/sjzxzjc.html',
        'http://www.yucheng.gov.cn/html/zhengfu/shendu.html',
        # 'http://www.yucheng.gov.cn/',
                  ]

    rules = (
        Rule(LinkExtractor(allow=r'/html/[a-z]+/[a-z]\.html$'), follow=True),
        Rule(LinkExtractor(allow=r'/html/[a-z]+/[a-z]+/\d+\.html$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/html/[a-z]+/\d+\.html$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'[a-z]+_\d+\.html'), follow=True),
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
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@class="info"]/text()').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="articlecontent"]/h3[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="MyContent"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

