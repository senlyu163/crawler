# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re
from scrapy_splash import SplashRequest

class A454CrawlSpider(CrawlSpider):
    name = '454_crawl'
    allowed_domains = ['linyou.gov.cn']
    start_urls = ['http://www.linyou.gov.cn/col/col1587/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/col/col\d+/index\.html\?number.*'), follow=True),
        Rule(LinkExtractor(allow=r'/col/col\d+/index\.html$'), follow=True),
        Rule(LinkExtractor(allow=r'/art/\d+/.*\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/col/.*pageNum=\d+'), follow=True),
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

            date = response.xpath('//*[@id="table"]/tr[2]/td[2]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="table"]/tr[3]/td/text()').extract_first()
            item['title'] = title

            contents = response.xpath('/html/body/div[4]/div/div[2]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="barrierfree_container"]/div[4]/div/div[1]/span[1]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="barrierfree_container"]/div[4]/p/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//*[@id="barrierfree_container"]/div[4]/div/div[2]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
