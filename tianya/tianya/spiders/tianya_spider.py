# -*- coding:utf-8 -*-

import scrapy
from tianya.items import TianyaItem

class tianyaSpider(scrapy.Spider):
    name = 'tianya'

    # allowed_domains = ['bbs.tianya.cn/']

    start_urls = ['http://bbs.tianya.cn/list-university-1.shtml']


    def parse(self, response):
        tbody = response.css('table tbody')[1]
        for tr in tbody.css('tr'):
            detail_link = tr.css('td a::attr(href)')[0].extract()
            # print tr.css('td a::text')[0].extract()
            detail_link = response.urljoin(detail_link)
            yield scrapy.Request(detail_link,callback=self.parse_detail)

        next_page = response.css('div.links a[rel]::attr(href)').extract_first()
        # print next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            
            # yield scrapy.Request(next_page,callback=self.parse)

    def parse_detail(self, response):
        item = TianyaItem()
        body =  response.css('div#doc')
        title = body.css('span.s_title span::text').extract_first()
        item['title'] = title
        # print title
        content = " ".join(body.css('div.bbs-content::text').extract())
        item['content'] = content
        item['url'] = response.url
        yield item