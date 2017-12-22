# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item,Field

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    chapter_name = Field()
    chapter_content = Field()
    pre_page =Field()
    page_key = Field()
    book_key = Field()
    pass

class BookItem(scrapy.Item):
    book_name = Field()
    book_key = Field()
    book_class =Field()
    book_img = Field()
    intro_info = Field()
    author = Field()
    pass
