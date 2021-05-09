# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re
from scrapy_splash import SplashRequest

class A188CrawlSpider(CrawlSpider):
    name = '188_crawl'
    allowed_domains = ['xxgk.guangshan.gov.cn']
    start_urls = [
        'http://xxgk.guangshan.gov.cn/zfwenjian/',
        'http://www.guangshan.gov.cn/zhongdianly/caizheng/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="gkbar left"]/ul//li'), follow=True),
        Rule(LinkExtractor(allow=r'/e/action/ShowInfo\.php\?classid=\d+&id=\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[1]/div[6]/div[4]/div[2]'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zhongdianly/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="newslist"]/ul//li'), callback='parse_item_2', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="content"]/div[2]/div[4]'), follow=True),
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

        date = response.xpath('/html/body/div[1]/div[6]/div[3]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[1]/div[6]/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="contentblock"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def parse_item_2(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="contentblock"]/div[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="contentblock"]/div[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="contentblock"]/div[5]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
