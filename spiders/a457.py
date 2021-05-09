# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A457Spider(CrawlSpider):
    name = '457'
    allowed_domains = ['changwu.gov.cn']
    start_urls = [
        'http://www.changwu.gov.cn/zwgk/',
        'http://www.changwu.gov.cn/info/iList.jsp?cat_id=10011',
    ]

    rules = (
        # Rule(LinkExtractor(allow=r'/info/iIndex\.jsp\?catalog_id=\d+&cat_id=\d+$'), follow=True),
        # Rule(LinkExtractor(allow=r'/gk/gk\d+/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="menus-item jc"]/ul[1]//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="menus-item zd"]/ul[1]//li'), follow=True),
        Rule(LinkExtractor(allow=r'/gk/.*/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?node_id=&site_id=CMScw&catalog_id=\d+&cur_page=\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/xw/[a-z]+/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/info/iList\.jsp\?cat_id=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'\?cat_id=\d+&cur_page=\d+$'), follow=True),
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

        date = response.xpath('//div[@class="tags"]/span[1]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@class="title"]/div/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="article"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
