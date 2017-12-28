#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import TutorialItem,BookItem
import re


reload(sys)
sys.setdefaultencoding("utf-8")


class ChapterSpider(CrawlSpider):
    # 爬虫名称
    name = "chapter"
    # 设置下载延时
    download_delay = 1
    # 允许域名
    allowed_domains = ["m.88dushu.com"]
    # 开始URL
    start_urls = [
        "http://m.88dushu.com/wapsort/1-50/"
    ]
    # 爬取规则,不带callback表示向该类url递归爬取
    nextpage = u'下一页'
    nextpage2 = u'下页'
    startRead = u'开始阅读'

    def __init__(self,book_key,ct, *args, **kwargs):
        self.book_key = book_key
        self.ct = ct
        self.start_urls = ["http://m.88dushu.com/mulu/"+book_key+"-1/"]
        self.rules = (
            Rule(SgmlLinkExtractor(allow=(r'http://m.88dushu.com/mulu/'+book_key+'-\d+/',), restrict_xpaths=('//a[text()="%s"]' % (self.nextpage))),follow=True),
            Rule(
                SgmlLinkExtractor(allow=(r'http://m.88dushu.com/book/'+book_key+'-\d+/',), restrict_xpaths=('//ul[@class="chapter" and not(@id)]')),
                callback='parse_content',follow=False),
        )

        super(ChapterSpider, self).__init__(*args, **kwargs)



    #解析小说详情
    def parse_book(self,response):
        try:
            item = BookItem()
            item["chapter_table"] = self.ct
            img = response.selector.xpath('//div[@class="block_img"]/img')[0]
            item["book_img"] = img.xpath('@src')[0].extract().decode('utf-8')
            item["book_name"] = img.xpath('@alt')[0].extract().decode('utf-8')
            item["book_class"] = '1'
            item["book_key"] = response.url[response.url.index('info/')+5:len(response.url)-1]
            intro_info = response.selector.xpath('//div[@class="intro_info"]')[0].extract().decode('utf-8')
            dr = re.compile(r'<[^>]+>', re.S)
            item["intro_info"] = dr.sub('', intro_info)
            item["author"] = response.selector.xpath('//div[@class="block_txt"]/p')[1].xpath('text()')[0].extract().decode('utf-8').replace('\n','').replace('\r','').replace('\t','').replace('作者：','')
        except:
            try:
                print(response.url+"解释出错")
            except:
                print("打印出错")
        else:
            yield item
    # 解析内容函数
    def parse_content(self, response):
        try:
            item = TutorialItem()
            item["chapter_table"] = self.ct
            # 当前URL
            title = response.selector.xpath('//div[@id="nr_title"]/text()')[0].extract().decode('utf-8')
            item['chapter_name'] = title

            #author = response.selector.xpath('//div[@id="news_info"]/span/a/text()')[0].extract().decode('utf-8')
            #item['author'] = author

            #releasedate = response.selector.xpath('//div[@id="news_info"]/span[@class="time"]/text()')[0].extract().decode('utf-8')
            #item['releasedate'] = releasedate

            news_body = response.selector.xpath('//a[@id="pt_prev"]')[0].xpath('@href')[0].extract().decode('utf-8')
            item["book_key"] = response.url[response.url.index('book/') + 5:response.url.index('-')]
            item["page_key"] = response.url[response.url.index('-') + 1:len(response.url)-1]
            endIndex = news_body.index(item["book_key"])
            if endIndex >= 0:
                item['pre_page'] = news_body[endIndex+6:len(news_body)-1]
            else:
                item['pre_page'] = ""

            news_body = response.selector.xpath('//div[@id="nr1"]')[0].extract().decode('utf-8')

            dr = re.compile(r'<[^>]+>', re.S)
            content = dr.sub('', news_body)

            endIndex = content.index("$(function()")
            if endIndex >= 0:
                item['chapter_content'] = content[0:endIndex-1]
            else:
                item['chapter_content'] = content
        except:
            print("解释章节出错了")
        else:
            yield item

