# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A169Spider(CrawlSpider):
    name = '169'
    allowed_domains = ['zfw.luanchuan.gov.cn']
    start_urls = ['http://zfw.luanchuan.gov.cn/#zwgk']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="lc_zk2"]'), follow=True),
        Rule(LinkExtractor(allow=r'zwgk\.php\?newsid=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?page=\d+&NodeId=.*'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="wm_news"]/ul//li/span'), callback='parse_item_2', follow=True),
        Rule(LinkExtractor(allow=r'/html/[a-z]+/\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 2})
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

        date = response.xpath('/html/body/div[4]/div[2]/div[2]/div/div[1]/div[1]/div[1]/text()').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[4]/div[2]/div[2]/div/div[1]/div[1]/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="mainhtml"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def parse_item_2(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[5]/div[2]/div[3]/span[1]/text()[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[5]/div[2]/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="xnd_cr5"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
