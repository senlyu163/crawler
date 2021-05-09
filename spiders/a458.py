# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A458Spider(CrawlSpider):
    name = '458'
    allowed_domains = ['snxunyi.gov.cn']
    start_urls = ['http://www.snxunyi.gov.cn/xxgk.htm']

    rules = (
        Rule(LinkExtractor(allow=r'/info/iList\.jsp\?tm_id=\d+&cat_id=\d+'), follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="zdxxgk_con"]/ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/gk/.*/\d+\.htm$'), callback='parse_item', follow=True),
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

        date = response.xpath('/html/body/div[2]/div[6]/div[2]/div[1]/div[3]/div/table/tr[2]/td[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[6]/div[2]/div[1]/div[3]/div/div/div[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="art-con"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
