# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class TaobaommPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        
        profileUrlPc = item["url"]
        yield scrapy.Request(profileUrlPc)