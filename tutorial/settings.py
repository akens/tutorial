# -*- coding: utf-8 -*-

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

# 禁止cookies,防止被ban
COOKIES_ENABLED = False
COOKIES_ENABLES = False

#图片保存地址
IMAGES_STORE = 'E:\\python\\pics'

# 设置Pipeline,此处实现数据写入文件
ITEM_PIPELINES = {
    'tutorial.pipelines.TutorialPipeline': 300
}

# 设置爬虫爬取的最大深度
DEPTH_LIMIT = 300

CONCURRENT_REQUESTS = 16

DUPEFILTER_DEBUG = True

#LOG_LEVEL = 'WARNING'