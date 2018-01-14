# -*- coding: utf-8 -*-
import scrapy
import json
import re
from TaobaoMM.items import TaobaommItem,AlbumItem,PicItem


class TaobaommspiderSpider(scrapy.Spider):
    name = 'TaoBaoMMspider'
    allowed_domains = ['mm.taobao.com']
    start_urls = ['https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8/']
    page = 1
    albumPage = 1
    
    def parse(self, response):
        data = json.loads(response.text)['data']['searchDOList']
        
        for each in data:
            mmitem = TaobaommItem()
            mmitem["realName"] = each['realName']
            mmitem["userId"] = each['userId']

            yield scrapy.Request("https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20="+str(mmitem["userId"])+"&page="+str(self.albumPage),callback=self.parse_model_album)
            
        self.page += 1
        


    def parse_model_album(self, response):
        for each in response.xpath("//div[@class='mm-photo-cell-middle']"):
            item = AlbumItem()
            #print(each.extract())
            #print(each.xpath("//a[@class='mm-first']/@href").extract()[0])
            url = each.xpath("//a[@class='mm-first']/@href").extract()[0]
            #print(url+"---------------")
            item['url'] = re.findall(r"album_id=(.+?)&album_flag",url)[0]

            yield scrapy.Request("https://"+url,callback=self.parse_model_album_list)

        self.albumPage+=1

    def parse_model_album_list(self, response):
        data = response.text
        u = response.xpath("//*[@id='J_AlbumFlag']/@data-url").extract()[0]
        yield scrapy.Request("https://"+u,callback=self.parse_model_album_book)

    def parse_model_album_book(self, response):
    	#print(response.text+"=================")
        u = response.xpath("//*[@id='J_JsonPanel']/@data-url").extract()[0]
        yield scrapy.Request("https://"+u,callback=self.parse_model_album_picture)
        # ff = response.text
        # ff = ff[11:-1]

        # data = json.loads(ff)['picList']

        # for each in data:
        #     picItem = PicItem()
        #     picItem['url'] = each['url']

        #     yield scrapy.Request("https:"+picItem['url'],callback=self.parse_model_album_picture)
    	#https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=362438816&album_id=10000794150&top_pic_id=0&cover=%2F%2Fimg.alicdn.com%2Fimgextra%2Fi4%2F362438816%2FTB1fSThMpXXXXasXXXXXXXXXXXX_!!0-tstar.jpg&page=1&_ksTS=1515861512183_154&callback=jsonp155
        
    def parse_model_album_picture(self, response):
    	ff = response.text
    	ff = ff[2:-1]
    	#print(str(ff)+"=================")
    	data = json.loads(ff)['picList']

    	for each in data:
            picItem = PicItem()
            picItem['url'] = "https:"+each['url']
            yield scrapy.Request(picItem['url'],callback=self.parse_model_album_picture_detail)
            #yield picItem
    	
    def parse_model_album_picture_detail(self, response):
    	userId = response.xpath("//*[@id='J_MmUserId']/@value").extract()[0]
    	picId = response.xpath("//*[@id='J_MmPicId']/@value").extract()[0]

    	yield scrapy.Request("https://mm.taobao.com/album/json/get_photo_data.htm?_input_charset=utf-8&pic_id="+ str(picId) +"&album_user_id="+str(userId),callback=self.getPhoto)
    	#print(response.text+"-------------------")

    def getPhoto(self, response):
        picItem = PicItem()
        data = json.loads(response.text)["photo_url"]
        
        print(data+"--------------------")
        picItem['url'] = "https:"+data
        yield picItem