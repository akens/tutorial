# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

import os
import random

from pip._vendor import requests
from scrapy import log
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

from tutorial.items import TutorialItem
from tutorial.settings import IMAGES_STORE
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class TutorialPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', mode='wb', encoding='utf-8')#数据存储到data.json
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                            host="172.16.1.221",
                                            db="reader",  # 数据库名
                                            user="root",  # 数据库用户名
                                            passwd="123456",  # 密码
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset="utf8",
                                            use_unicode=False
                                            )
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self,spider):
        try:
            query = self.dbpool.runInteraction(self._update_book, spider.book_key)
            query.addErrback(self.handle_error)
        except:
            print("更新出错")

    def process_item(self, item, spider):
        try:
            if isinstance(item,TutorialItem):
                query = self.dbpool.runInteraction(self._insert_chapter, item)
                query.addErrback(self.handle_error)
                pass
            elif isinstance(item,str):
                print(item)
            else:
                query = self.dbpool.runInteraction(self._insert_book, item)
                query.addErrback(self.handle_error)
                pass
        except:
            print("保存出错")
        return item

    def _update_book(self,tb,item):
        tb.execute(
            "update book set inited = 1 WHERE book_key = %s", \
            (item))
        log.msg("Item data in db: %s" % item, level=log.DEBUG)

    def _insert_book(self, tb, item):
        item['book_img'] = self.save_img(item)
        tb.execute("insert ignore into book (book_name,book_key,book_class,book_img,intro_info,author,chapter_table) values (%s,%s,%s,%s,%s,%s,%s)", \
                   (item["book_name"],item["book_key"],item["book_class"],item["book_img"],item["intro_info"],item["author"],item["chapter_table"]))
        log.msg("Item data in db: %s" % item, level=log.DEBUG)

    def _save_content(self,name,content):
        dir_path = '{}'.format('F:\\reader\\chapter')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        with open('{}//{}.txt'.format(dir_path, name), 'wb') as f:
            f.write(content)
            f.close()

    def _insert_chapter(self, tb, item):
        self._save_content(item["book_key"]+"-"+item["page_key"],item["chapter_content"])
        tb.execute("insert ignore into "+item["chapter_table"]+" (chapter_name, pre_page,book_key,page_key) values (%s, %s, %s,%s)", \
                   (item["chapter_name"], item["pre_page"], item["book_key"],item["page_key"]))
        log.msg("Item data in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)

    def save_img(self,item):
        header = {
            'USER-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Cookie': 'b963ef2d97e050aaf90fd5fab8e78633',
            # 需要查看图片的cookie信息，否则下载的图片无法查看
        }
        # 所有图片放在一个文件夹下
        dir_path = '{}'.format(IMAGES_STORE)
        if not os.path.exists(dir_path) and len(item['book_img']) > 0:
            os.mkdir(dir_path)
        if len(item['book_img']) > 0:
                file_name = item['book_key']
                file_path = '{}//{}.jpg'.format(dir_path, file_name)
                if os.path.isfile(file_path):
                    return file_name
                    #file_name = '00000'+file_name + random.randint(10000,999999)
                with open('{}//{}.jpg'.format(dir_path, file_name), 'wb') as f:
                    req = requests.get(item['book_img'], headers=header,verify=False)
                    f.write(req.content)
                return file_name