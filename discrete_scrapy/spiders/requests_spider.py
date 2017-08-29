# coding=utf8
import re
from scrapy.selector import Selector
from base_spider import BaseSpider
from discrete_scrapy.login import is_login,login,cookielib
from scrapy_redis.spiders import RedisSpider
import scrapy
import copy
import time
import  requests,json
from redis import Redis

tt = Redis()
tt.sadd('test','fdsfdsfdsf','huagnkaijie')

class MZhanSpider(BaseSpider):

    name = 'mzhan_request_spider'

    start_urls = [
        'http://www.missevan.com'
    ]
    host_url = 'http://www.missevan.com'
    audio_host = 'http://static.missevan.com/'
    uid_prefix = '9999'

    def __init__(self):
        self.r = Redis()
        self.f = open('sound_url.txt', 'a')

    def start_requests(self):
        if not is_login():
            login()
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                cookies=cookielib.LWPCookieJar(filename='mzhan_cookies'),
                callback=self.parse_category,
                errback=self.handle_error
            )
    def parse_category(self, response):
        metadata = {}
        sel = Selector(response)
        category = sel.xpath(
            '//div[@class="vw-topcatalog-container"]//div[@class="vw-topcatalog-item fc-topcatalog-item"]')
        for sub_category in category:
            c_1 = sub_category.xpath('./a/@title').extract()
            sub = sub_category.xpath('./div/a')
            # print c_1[0]
            if c_1:
                metadata['audio_category_first']=c_1[0]
            for node in sub:
                url = node.xpath('./@href').extract()

                if url:
                    full_url = self.host_url + url[0]
                    c_2 = node.xpath('./@title').extract()
                    # print '    ', url[0]
                    # print '    ', c_2[0]
                    if c_2:
                        metadata['audio_category_last']=c_2[0]
                    m = copy.deepcopy(metadata)
                    yield scrapy.Request(
                        url=full_url,
                        meta={'audiodata':m},
                        cookies=cookielib.LWPCookieJar(filename='mzhan_cookies'),
                        callback=self.parse_page,
                        errback=self.handle_error,
                        priority=3
                    )

    def parse_page(self, response):
        metadata = response.meta['audiodata']
        model_url = 'http://www.missevan.com/sound/m?id=%s&p=%s'
        sel = Selector(response)
        category_id = response.url.split('/')[-1]
        total = 0
        page_sum_node = sel.xpath('//li[@class="last"]/a/@href').extract()
        if page_sum_node:
            total = page_sum_node[0].split('=')[-1]
            print response.url
        if total != 0:
            for p in range(1,int(total)+1):
                url = model_url % (category_id, p)
                m = copy.deepcopy(metadata)
                yield scrapy.Request(
                    url=url,
                    meta={'audiodata': m},
                    cookies=cookielib.LWPCookieJar(filename='mzhan_cookies'),
                    callback=self.parse_cover_title,
                    errback=self.handle_error,
                    priority=5
                )

    def parse_cover_title(self, response):
        metadata = response.meta['audiodata']
        sel = Selector(response)
        nodes = sel.xpath('//div[@class="vw-subcatalog-contant fc-leftcontent-block floatleft"]/div/a')
        print response.url,'=========='
        for node in nodes:
            url = node.xpath('./@href').extract()
            if url:
                #url = self.host_url+url[0].strip()
                print url,'---------------'
                sound_id = url[0].strip().split('/')[-1]
                print sound_id

                url = 'http://www.missevan.com/sound/getsoundlike?type=7&sound_id=%s' % sound_id
                print url
                #self.r.sadd('mzhan:soundurl', url)
                if url+'\n' not in self.f:
                    self.f.writelines(url+'\n')

    def close(spider, reason):
        spider.f.close()