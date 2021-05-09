# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from ..items import ScrapySpiderItem
# from ..utils import extract_CN_from_content
# import re
#
# class A130CrawlSpider(CrawlSpider):
#     name = '130_crawl'
#     allowed_domains = ['susong.gov.cn']
#     start_urls = ['http://www.susong.gov.cn/public/User/PageList.aspx?unitId=4&clsid=0&page=1']
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/public/User/DisplayInfo\.aspx\?ItemId=\d+'), callback='parse_item', follow=True),
#         Rule(LinkExtractor(restrict_xpaths='//div[@class="Pages"]/span[3]'), follow=True),
#         Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
#
#     def parse_item(self, response):
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('//*[@id="container"]/div/div[2]/table/tr[3]/td[4]').extract_first()
#         date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('//*[@id="container"]/div/div[2]/h2/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@id="artibody"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item
