# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A461Spider(CrawlSpider):
    name = '461'
    allowed_domains = ['chengcheng.gov.cn']
    start_urls = ['http://www.chengcheng.gov.cn/zwgk/']

    rules = (
        Rule(LinkExtractor(allow=r'/info/iIndex\.jsp\?catalog_id=\d+&cat_id=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/gk/bmgk\d+/bmgk\d+/\d+\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?node_id=&site_id=CMScc&catalog_id=\d+&cur_page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
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
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[4]/div/div[3]/span[1]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[4]/div/div[2]/div/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="article"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            print("There has no correct time format.")
