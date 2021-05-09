# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests
from ..utils import extract_CN_from_content
from ..utils import add_url_to_start_url
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A459Spider(CrawlSpider):
    name = '459'
    allowed_domains = ['snchunhua.gov.cn']
    start_urls = [
        "http://www.snchunhua.gov.cn/zfbg/index.jhtml",
        "http://www.snchunhua.gov.cn/jsjf/index.jhtml",
    ]

    zfwj = "http://www.snchunhua.gov.cn/zfwj/index_{}.jhtml"
    for n in range(17):
        url = zfwj.format(n+1)
        start_urls.append(url)

    wxgk = "http://www.snchunhua.gov.cn/wxgk/index_{}.jhtml"
    for n in range(8):
        url = wxgk.format(n+1)
        start_urls.append(url)

    zyhy = "http://www.snchunhua.gov.cn/zyhy/index_{}.jhtml"
    for n in range(7):
        url = zyhy.format(n+1)
        start_urls.append(url)

    zcfg = "http://www.snchunhua.gov.cn/zcfg/index_{}.jhtml"
    for n in range(4):
        url = zcfg.format(n+1)
        start_urls.append(url)

    ghjh = "http://www.snchunhua.gov.cn/ghjh/index_{}.jhtml"
    for n in range(2):
        url = ghjh.format(n+1)
        start_urls.append(url)

    def add_url_to_start_url(url, index, start_urls):
        url_template = url[:-6] + "_{}" + url[-6:]
        for n in range(index):
            complete_url = url_template.format(n+1)
            start_urls.append(complete_url)

    add_url_to_start_url(url="http://www.snchunhua.gov.cn/zdxm/index.jhtml", index=4, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/czgk/index.jhtml", index=40, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/zrkh/index.jhtml", index=5, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/ggzy/index.jhtml", index=10, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/ggfw/index.jhtml", index=14, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/ggjg/index.jhtml", index=7, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/xhjbh/index.jhtml", index=29, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/shgy/index.jhtml", index=13, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/yjgl/index.jhtml", index=5, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/rdhy/index.jhtml", index=4, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/tjxx/index.jhtml", index=3, start_urls=start_urls)
    add_url_to_start_url(url="http://www.snchunhua.gov.cn/tabl/index.jhtml", index=8, start_urls=start_urls)


    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="box_tab"]/table//tr/td[1]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/[a-z]+/\d+\.jhtml'), callback='parse_item', follow=True),
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

        date = response.xpath('//*[@id="neirong"]/table/tr[3]/td[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@id="neirong"]/p/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="vfd"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
