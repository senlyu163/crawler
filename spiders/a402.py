# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A402Spider(CrawlSpider):
    name = '402'
    allowed_domains = ['menglian.gov.cn']
    start_urls = ['http://www.menglian.gov.cn/xxgklby_list.jsp?urltype=egovinfo.EgovTreeURl&wbtreeid=1100&type=egovinfodeptsubcattree&sccode=ml&subtype=1&dpcode=P004&gilevel=1']

    rules = (
        Rule(LinkExtractor(allow=r'info/.*\.htm'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?ainfolist\d+t=\d+&ainfolist\d+p=\d+&ainfolist\d+c=\d+&urltype=egovinfo\.EgovTreeURl&wbtreeid=\d+&type=egovinfodeptsubcattree&sccode=ml&subtype=\d+&dpcode=P\d+&gilevel=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 1.5})
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

        date = response.xpath('/html/body/div[5]/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[5]/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[3]/td[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="vsb_content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item