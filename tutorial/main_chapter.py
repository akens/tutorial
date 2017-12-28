import codecs
from multiprocessing import Process

import time

import MySQLdb
from scrapy import cmdline
from twisted.enterprise import adbapi


def run_spider(book_key,chapter_name):
    cmdline.execute(("scrapy crawl chapter -a book_key="+book_key+" -a ct="+chapter_name).split())

if __name__ == "__main__":
    process_list = []
    db = MySQLdb.connect("172.16.1.221", "root", "123456", "reader")
    cursor = db.cursor()
    sql = "SELECT book_key,chapter_table FROM book WHERE inited = 0"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            book_key = row[0]
            chapter_table = row[1]
            if process_list.__len__() < 50:
                process = Process(target=run_spider, args=(book_key,chapter_table,))
                process_list.append(process)
                process.start()
            else:
                while True:
                    e = 0
                    for th in process_list:
                        if not th.is_alive():
                            del process_list[e]
                            e = 0
                            break
                        e = e + 1
                    if e <= 0:
                        process = Process(target=run_spider, args=(book_key, chapter_table,))
                        process_list.append(process)
                        process.start()
                        break
                    time.sleep(1)
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