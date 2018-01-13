import codecs
from multiprocessing import Process

import time

import MySQLdb
import os

import shutil
from scrapy import cmdline
from twisted.enterprise import adbapi


def run_spider(book_key,chapter_name):
    cmdline.execute(("scrapy crawl chapter -a book_key="+book_key+" -a ct="+chapter_name).split())

if __name__ == "__main__":
    process_list = []
    db = MySQLdb.connect("172.16.1.221", "root", "123456", "reader")
    cursor = db.cursor()
    sql = "SELECT book_key,page_key,chapter_content FROM chapter_1"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            try:
                dir_path = '{}'.format('F:\\reader\\chapter\\' + row[0])
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                new_file = '{}//{}.txt'.format(dir_path, row[0] + '-' + row[1])
                if row[2] == "":
                    old_path = '{}'.format('F:\\reader\\chapter')
                    old_file = '{}//{}.txt'.format(old_path, row[0]+'-'+row[1])
                    shutil.move(old_file,new_file)
                    os.remove(old_file)
                else:
                    with open(new_file, 'wb') as f:
                        f.write(row[2])
                        f.close()
            except:
                print "转移文件出错"
    except:
        print "Error: unable to fecth data"

    db.close()

    e = process_list.__len__()
    while True:
        for th in process_list:
            if not th.is_alive():
                e -= 1
        if e <= 0:
            break
        time.sleep(1)