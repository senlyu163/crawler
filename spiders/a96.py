# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A96Spider(CrawlSpider):
    name = '96'
    allowed_domains = ['cyhq.gov.cn']
    start_urls = [#'http://www.cyhq.gov.cn/channel/cyhq/col30093f.html',
                  # 'http://www.cyhq.gov.cn/channel/cyhq/col17962f.html',
    # 'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30093'
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30093',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=25&showpagenum=true&fid=18535',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=25&showpagenum=true&fid=18536',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=25&showpagenum=true&fid=17965',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=25&showpagenum=true&fid=17960',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=18529',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=18530',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=18532',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=18534',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30093',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30039',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30040',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30041',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30042',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30043',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30044',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30045',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30046',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30047',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30048',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30049',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30050',
        'http://www.cyhq.gov.cn/active/fpage_1.jsp?psize=20&showpagenum=true&fid=30051',
    ]

    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//div[@id="hlcms_4a2u80s2u3fk0ze"]/ul'), follow=True),
        # Rule(LinkExtractor(allow=r'/information/cyhq\d+/msg\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//table[@class="recordlist"]//tr//td'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?psize=\d+&showpagenum=true&fid=\d+&pos=\d+'), follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//div[@id="hlcms_xmcg7k4c9vqfeo8"]/ul//li'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    # def _build_request(self, rule, link):
    #     r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 0.5})
    #     r.meta.update(rule=rule, link_text=link.text)
    #     return r
    #
    # def _requests_to_follow(self, response):
    #     # if not isinstance(response, HtmlResponse):
    #     #     return
    #     seen = set()
    #     for n, rule in enumerate(self._rules):
    #         links = [lnk for lnk in rule.link_extractor.extract_links(response)
    #                  if lnk not in seen]
    #         if links and rule.process_links:
    #             links = rule.process_links(links)
    #         for link in links:
    #             seen.add(link)
    #             r = self._build_request(n, link)
    #             yield rule.process_request(r)

    def parse_item(self, response):
        # print(">>>>>", response.url)
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//div[@id="otherinfo"]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//div[@id="title"]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
