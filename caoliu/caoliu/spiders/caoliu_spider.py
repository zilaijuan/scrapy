# -*- coding:utf-8 -*-

import scrapy
from caoliu.items import CaoliuItem

class caoliuSpider(scrapy.Spider):
    name = 'caoliu'

    # allowed_domains = ['bbs.tianya.cn/']

    start_urls = [
                    'http://liuyouba.tk/thread0806.php?fid=2',
                    'http://liuyouba.tk/thread0806.php?fid=15',
                    'http://liuyouba.tk/thread0806.php?fid=21',
                    'http://liuyouba.tk/thread0806.php?fid=22',
                    'http://liuyouba.tk/thread0806.php?fid=7'
                 ]


    def parse(self, response):
        item = CaoliuItem()
        category = response.css('div.t3 table tr td a::text')[1].extract()
        # print category
        for tr in response.css('tr.tr3'):
            title = tr.css('td h3 a::text').extract_first()

            url = tr.css('td h3 a::attr(href)').extract_first()
            url = response.urljoin(url)
            print url
            if title is not None:
                item['category'] = category
                item['title'] = title
                item['url'] = url
                yield item
        
        next_page = response.css('div.pages a::attr(href)').extract()
        
        next_page = response.urljoin(next_page[-2])
        if next_page is not None:
            yield scrapy.Request(next_page,callback=self.parse)

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