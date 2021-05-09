# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re
from scrapy_splash import SplashRequest

class A205CrawlSpider(CrawlSpider):
    name = '205_crawl'
    allowed_domains = ['djk.gov.cn']
    start_urls = ['http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/list_3978.shtml']

    url_template = "http://www.djk.gov.cn/zwgk/xxgkzl/xxgkml/list_3978_{}.shtml"
    for n in range(24):
        url = url_template.format(n+1)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.shtml'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'list_\d+_\d+\.shtml'), follow=True),
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

            date = response.xpath('/html/body/div[3]/div[1]/div/table/tr[1]/td[3]').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[3]/div[2]/h1/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="TRS_Editor"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[3]/div/div/div[1]/span[1]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[3]/div/div/h4/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//*[@id="fontzoom"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
