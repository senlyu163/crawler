# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A341Spider(CrawlSpider):
    name = '341'
    allowed_domains = ['yinjiang.gov.cn']
    start_urls = [
        'http://www.yinjiang.gov.cn/xxgk/zxgk/zcwj/',
        'http://www.yinjiang.gov.cn/xxgk/zdxxgk/xzqlgk/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/xxgk/[a-z]+/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="right_list f_r f14"]/dl/dd/ul//li'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/xxgk/[a-z]+/[a-z]+/[a-z]+/$'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        for su in self.start_urls:
            yield SplashRequest(url=su, args={"wait": 2})

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

        date = response.xpath('//*[@id="fbsj"]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[4]/div[1]/div[2]/h2/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="zx_content t_l"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
