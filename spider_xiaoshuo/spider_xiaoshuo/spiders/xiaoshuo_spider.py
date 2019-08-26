# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.request import urlopen
from pymongo import MongoClient

mongo=MongoClient()
db=mongo["yz"]["xiaoshuo"]

re_paragraph = re.compile('(?<=<p>).*?(?=</p>)')

class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo_spider'
    allowed_domains = ['jinyongwang.com']
    start_urls = [
        'http://www.jinyongwang.com/fei/',#�ɺ��⴫
        'http://www.jinyongwang.com/xue/',#ѩɽ�ɺ�
        'http://www.jinyongwang.com/lian/',#���Ǿ�
        'http://www.jinyongwang.com/tian/',#�����˲�
        'http://www.jinyongwang.com/she/',#���Ӣ�۴�
        'http://www.jinyongwang.com/bai/',#����Х����
        'http://www.jinyongwang.com/lu/',#¹����
        'http://www.jinyongwang.com/xiao/',#Ц������
        'http://www.jinyongwang.com/shu/',#�齣����¼
        'http://www.jinyongwang.com/shen/',#�������
        'http://www.jinyongwang.com/xia/',#������
        'http://www.jinyongwang.com/yi/',#����������
        'http://www.jinyongwang.com/bi/',#��Ѫ��
        'http://www.jinyongwang.com/yuan/',#ԧ�쵶
        'http://www.jinyongwang.com/yue/',#ԽŮ��
    ] #��ӹ��ȫ��С˵
 
    #��ȡС˵�½ڵ�URL
    def parse(self, response):

        cnt_url = "/".join(response._url.strip("/").split("/")[:-1])
        name = response.xpath('//div[@class="pu_breadcrumb"]//h3[@class="set"]/font/text()').extract_first()
        chapter_names = response.xpath('//ul[@class="mlist"]//li/a/text()').extract()
        chapter_urls = response.xpath('//ul[@class="mlist"]//li/a/@href').extract()
        
        chapters = []
        for chapter_name, chapter_url in zip(chapter_names, chapter_urls):
            chapter_name = chapter_name.replace("\u3000", " ")
            response = urlopen(cnt_url + chapter_url)
            html = response.read().decode("utf-8")
            texts = re_paragraph.findall(str(html))
            chapters.append({"name": chapter_name, "content": "\n".join(texts)})
        
        db.save({"book_name": name, "chapters": chapters})
