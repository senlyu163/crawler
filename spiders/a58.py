# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A58Spider(CrawlSpider):
    name = '58'
    allowed_domains = ['scx.sxxz.gov.cn']
    start_urls = ['http://scx.sxxz.gov.cn/scxzw/zwgk/xxgknb/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li/ul/li[4]/dl//dd'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li/ul/li[9]/dl//dd'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li/ul/li[10]/dl//dd'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div/div[1]/ul/li[5]/ul/li/ul//li'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="searchsection"]/div[2]/a[3]'), follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html/'), follow=True),
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

            date = response.xpath('/html/body/div[2]/div[1]/div/div[1]/p').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[2]/div[1]/div/div[1]/h2/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="article-con"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[2]/div/div/div[1]/table/tr[5]/td[2]/span[3]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[2]/div/div/div[1]/table/tr[4]/td/span[3]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="article-con"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item

