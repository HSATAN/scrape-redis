# coding=utf8

import scrapy
import logging
class BaseSpider(scrapy.Spider):

    def handle_error(self,**kwargs):
        logging.error(str(kwargs))