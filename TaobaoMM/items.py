# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaommItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userId = scrapy.Field()
    realName = scrapy.Field()


class AlbumItem(scrapy.Item):
	url = scrapy.Field()


class PicItem(scrapy.Item):
	url = scrapy.Field()
	
		
