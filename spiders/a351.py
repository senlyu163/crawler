# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A351Spider(CrawlSpider):
    name = '351'
    allowed_domains = ['gzal.gov.cn']
    start_urls = ['http://www.gzal.gov.cn/zwgk/xxgkml/jcxxgk/jgsz/zfgzbm/index.html']

    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//ul[@class="browser filetree treeview"]//li/ul//li/ul/li[1]/span'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/xxgkml/[a-z]+/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/xxgkml/[a-z]+/[a-z]+/[a-z]+/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 1})
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

        date = response.xpath('//*[@id="textCont"]/div[1]/span[2]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="textCont"]/h3/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="textBox"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        year = date[:4]
        if int(year) >= 2015 and int(year) <= 2019:
            return item
