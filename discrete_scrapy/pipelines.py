# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from discrete_scrapy.utils.db import BaseDB
from common import *


class MzhanPipeline(object):

    def __init__(self):
        self.db = BaseDB()

    def process_item(self, item, spider):
        print '---------------------------------------------------------------'

        album_sql = ''
        audio_sql = ''
        user_sql = ''

        data = dict(item)
        album_columns = ''
        album_values = ''
        for key, value in album_item_to_tabel.items():
            try:
                album_values = album_values + ',' + "'%s'" % item[key]
                album_columns = album_columns + ',' + value
            except:pass
        if album_values:
            album_sql = '(%s)' % album_columns.strip(',') + '  VALUES(%s)' % album_values.strip(',')

        user_columns = ''
        user_values = ''
        for key, value in upper_item_to_tabel.items():
            try:
                user_values = user_values + ',' + "'%s'" % item[key]
                user_columns = user_columns + ',' + value
            except Exception as e:
                print e
                pass
        if user_values:
            user_sql = '(%s)' %user_columns.strip(',') + '  VALUES(%s)' % user_values.strip(',')
        audio_columns = ''
        audio_values = ''
        for key, value in audio_item_to_table.items():
            try:
                audio_values = audio_values + ',' + "'%s'" % item[key]
                audio_columns = audio_columns + ',' + value
            except:
                pass
        if audio_values:
            audio_sql = '(%s)' % audio_columns.strip(',') + '  VALUES(%s)' % audio_values.strip(',')
        if item['audio_tags']:
            for tag in item['audio_tags']:
                tag_sql = "(audio_id,tag_name,tag_id,touch_time) VALUES('%s','%s','%s','%s')" % (item['audio_id'], tag['name'], tag['id'], item['touch_time'])
                self.db.query('mzhan_tag', tag_sql)


        print album_sql
        print user_sql
        print audio_sql
        # try:
        self.db.query('mzhan_user',user_sql)
        # except Exception as e:
        #     print e
        if album_sql:
            # try:
            self.db.query('mzhan_album', album_sql)
            # except Exception as e:
            #     print e
        if audio_sql:
            #try:
            self.db.query('mzhan_audio', audio_sql)
            #except Exception as e:
                #print

        return item

    def spider_closed(self,spider):
        self.db.close()

