#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import TutorialItem,BookItem
import re

reload(sys)
sys.setdefaultencoding("utf-8")


class ListSpider(CrawlSpider):
    # 爬虫名称
    name = "tutorial"
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
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'http://m.88dushu.com/wapsort/1-[0-1][0-9]/',), restrict_xpaths=('//a[text()="%s"]' %(nextpage2)))),
        Rule(SgmlLinkExtractor(allow=(r'http://m.88dushu.com/info/\d+/',),restrict_xpaths=('//div[@class="block_img"]')),callback='parse_book',follow=True),
        Rule(SgmlLinkExtractor(allow=(r'http://m.88dushu.com/mulu/\d+/',), restrict_xpaths=('//a[text()="%s"]' % (startRead))),follow=True),
        Rule(SgmlLinkExtractor(allow=(r'http://m.88dushu.com/mulu/\d+-\d+/',), restrict_xpaths=('//a[text()="%s"]' % (nextpage))),follow=True),
        Rule(
            SgmlLinkExtractor(allow=(r'http://m.88dushu.com/book/\d+-\d+/',), restrict_xpaths=('//ul[@class="chapter" and not(@id)]')),
            callback='parse_content',follow=False),
    )

    allows = [r'http://m.88dushu.com/wapsort/1-[1-9]/',
              r'http://m.88dushu.com/wapsort/1-1[0-9]/',
              r'http://m.88dushu.com/wapsort/1-2[0-9]/',
              r'http://m.88dushu.com/wapsort/1-3[0-9]/',
              r'http://m.88dushu.com/wapsort/1-4[0-9]/',
              r'http://m.88dushu.com/wapsort/1-5[0-9]/',
              r'http://m.88dushu.com/wapsort/1-6[0-9]/',
              r'http://m.88dushu.com/wapsort/1-7[0-9]/',
              r'http://m.88dushu.com/wapsort/1-8[0-9]/',
              r'http://m.88dushu.com/wapsort/1-9[0-9]/',
              r'http://m.88dushu.com/wapsort/1-10[0-9]/',
              r'http://m.88dushu.com/wapsort/1-11[0-9]/',
              r'http://m.88dushu.com/wapsort/1-12[0-9]/',
              r'http://m.88dushu.com/wapsort/1-13[0-9]/',
              r'http://m.88dushu.com/wapsort/1-14[0-9]/',
              r'http://m.88dushu.com/wapsort/1-15[0-9]/',
              r'http://m.88dushu.com/wapsort/1-16[0-9]/',
              r'http://m.88dushu.com/wapsort/1-17[0-9]/',
              r'http://m.88dushu.com/wapsort/1-18[0-9]/',
              r'http://m.88dushu.com/wapsort/1-19[0-9]/',
              r'http://m.88dushu.com/wapsort/1-20[0-9]/',
              r'http://m.88dushu.com/wapsort/1-21[0-9]/',
              r'http://m.88dushu.com/wapsort/1-22[0-9]/',
              r'http://m.88dushu.com/wapsort/1-23[0-9]/',
              r'http://m.88dushu.com/wapsort/1-24[0-9]/',
              r'http://m.88dushu.com/wapsort/1-25[0-9]/',
              r'http://m.88dushu.com/wapsort/1-26[0-9]/',
              r'http://m.88dushu.com/wapsort/1-27[0-9]/',
              r'http://m.88dushu.com/wapsort/1-28[0-9]/',
              r'http://m.88dushu.com/wapsort/1-29[0-9]/',
              r'http://m.88dushu.com/wapsort/1-30[0-9]/',
              r'http://m.88dushu.com/wapsort/1-31[0-9]/',
              r'http://m.88dushu.com/wapsort/1-32[0-9]/',
              r'http://m.88dushu.com/wapsort/1-33[0-9]/',
              r'http://m.88dushu.com/wapsort/1-34[0-9]/',
              r'http://m.88dushu.com/wapsort/1-35[0-9]/',
              r'http://m.88dushu.com/wapsort/1-36[0-9]/',
              r'http://m.88dushu.com/wapsort/1-37[0-9]/',
              r'http://m.88dushu.com/wapsort/1-38[0-9]/',
              r'http://m.88dushu.com/wapsort/1-39[0-9]/',
              r'http://m.88dushu.com/wapsort/1-40[0-9]/',
              r'http://m.88dushu.com/wapsort/1-41[0-9]/',
              r'http://m.88dushu.com/wapsort/1-42[0-9]/',
              r'http://m.88dushu.com/wapsort/1-43[0-9]/']

    urls = ["http://m.88dushu.com/wapsort/1-1/",
            "http://m.88dushu.com/wapsort/1-10/",
            "http://m.88dushu.com/wapsort/1-20/",
            "http://m.88dushu.com/wapsort/1-30/",
            "http://m.88dushu.com/wapsort/1-40/",
            "http://m.88dushu.com/wapsort/1-50/",
            "http://m.88dushu.com/wapsort/1-60/",
            "http://m.88dushu.com/wapsort/1-70/",
            "http://m.88dushu.com/wapsort/1-80/",
            "http://m.88dushu.com/wapsort/1-90/",
            "http://m.88dushu.com/wapsort/1-100/",
            "http://m.88dushu.com/wapsort/1-110/",
            "http://m.88dushu.com/wapsort/1-120/",
            "http://m.88dushu.com/wapsort/1-130/",
            "http://m.88dushu.com/wapsort/1-140/",
            "http://m.88dushu.com/wapsort/1-150/",
            "http://m.88dushu.com/wapsort/1-160/",
            "http://m.88dushu.com/wapsort/1-170/",
            "http://m.88dushu.com/wapsort/1-180/",
            "http://m.88dushu.com/wapsort/1-190/",
            "http://m.88dushu.com/wapsort/1-200/",
            "http://m.88dushu.com/wapsort/1-210/",
            "http://m.88dushu.com/wapsort/1-220/",
            "http://m.88dushu.com/wapsort/1-230/",
            "http://m.88dushu.com/wapsort/1-240/",
            "http://m.88dushu.com/wapsort/1-250/",
            "http://m.88dushu.com/wapsort/1-260/",
            "http://m.88dushu.com/wapsort/1-270/",
            "http://m.88dushu.com/wapsort/1-280/",
            "http://m.88dushu.com/wapsort/1-290/",
            "http://m.88dushu.com/wapsort/1-300/",
            "http://m.88dushu.com/wapsort/1-310/",
            "http://m.88dushu.com/wapsort/1-320/",
            "http://m.88dushu.com/wapsort/1-330/",
            "http://m.88dushu.com/wapsort/1-340/",
            "http://m.88dushu.com/wapsort/1-350/",
            "http://m.88dushu.com/wapsort/1-360/",
            "http://m.88dushu.com/wapsort/1-370/",
            "http://m.88dushu.com/wapsort/1-380/",
            "http://m.88dushu.com/wapsort/1-390/",
            "http://m.88dushu.com/wapsort/1-400/",
            "http://m.88dushu.com/wapsort/1-410/",
            "http://m.88dushu.com/wapsort/1-420/",
            "http://m.88dushu.com/wapsort/1-430/"]

    table_names = ["chapter_1",
                   "chapter_1",
                   "chapter_1",
                   "chapter_1",
                   "chapter_2",
                   "chapter_2",
                   "chapter_2",
                   "chapter_2",
                   "chapter_3",
                   "chapter_3",
                   "chapter_3",
                   "chapter_3",
                   "chapter_4",
                   "chapter_4",
                   "chapter_4",
                   "chapter_4",
                   "chapter_5",
                   "chapter_5",
                   "chapter_5",
                   "chapter_5",
                   "chapter_6",
                   "chapter_6",
                   "chapter_6",
                   "chapter_6",
                   "chapter_7",
                   "chapter_7",
                   "chapter_7",
                   "chapter_7",
                   "chapter_8",
                   "chapter_8",
                   "chapter_8",
                   "chapter_8",
                   "chapter_9",
                   "chapter_9",
                   "chapter_9",
                   "chapter_9",
                   "chapter_10",
                   "chapter_10",
                   "chapter_10",
                   "chapter_10",
                   "chapter_11",
                   "chapter_11",
                   "chapter_11",
                   "chapter_11"]

    def __init__(self,process_idx, *args, **kwargs):
        self.idx = int(process_idx)
        self.start_urls = [self.urls[self.idx]]
        self.rules = (
            Rule(SgmlLinkExtractor(allow=(self.allows[self.idx],), restrict_xpaths=('//a[text()="%s"]' %(self.nextpage2)))),
            Rule(SgmlLinkExtractor(allow=(r'http://m.88dushu.com/info/\d+/',),restrict_xpaths=('//div[@class="block_img"]')),callback='parse_book',follow=True),
            Rule(SgmlLinkExtractor(allow=(r'http://m.88dushu.com/mulu/\d+/',), restrict_xpaths=('//a[text()="%s"]' % (self.startRead))),follow=True),
            Rule(SgmlLinkExtractor(allow=(r'http://m.88dushu.com/mulu/\d+-\d+/',), restrict_xpaths=('//a[text()="%s"]' % (self.nextpage))),follow=True),
            Rule(
                SgmlLinkExtractor(allow=(r'http://m.88dushu.com/book/\d+-\d+/',), restrict_xpaths=('//ul[@class="chapter" and not(@id)]')),
                callback='parse_content',follow=False),
        )
        super(ListSpider, self).__init__(*args, **kwargs)
    #解析小说详情
    def parse_book(self,response):
        try:
            item = BookItem()
            item["chapter_table"] = self.table_names[self.idx]
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
            item["chapter_table"] = self.table_names[self.idx]
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

