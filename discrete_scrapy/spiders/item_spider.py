# coding=utf8

from scrapy_redis.spiders import RedisSpider
from . import defaults
import copy,json,time,re
import scrapy
from discrete_scrapy.items import MzhanItem
from base_spider import BaseSpider

class ItemSpider(RedisSpider, BaseSpider):

    name = 'item_spider'
    redis_key = 'mzhan:start_urls'
    host_url = 'http://www.missevan.com'
    audio_host = 'http://static.missevan.com/'
    uid_prefix = '9999'



    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ItemSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data = response.text
        sound_id = response.url.split('=')[-1]
        metadata = {}
        metadata['audio_main_url'] = 'http://www.missevan.com/sound/player?id=%s' % sound_id
        sound_url = 'http://www.missevan.com/sound/getsound?soundid=%s' % sound_id
        if data:
            albums = None
            try:
                data = json.loads(data)
                albums = data['successVal']['albums'][0]
            except Exception as e:
                print e
            if albums:
                albums_id = self.uid_prefix + str(albums['id'])
                albums_name = albums['title']
                albums_create_time = albums['create_time']
                albums_create_user_id = self.uid_prefix + str(albums['user_id'])
                albums_cover_image = albums['front_cover']
                albums_last_update_time = albums['last_update_time']
                metadata['album_id'] = albums_id
                metadata['album_name'] = albums_name
                metadata['album_create_time'] = self.getTime(albums_create_time)
                metadata['album_update_time'] = self.getTime(albums_last_update_time)
                metadata['album_create_user_id'] = albums_create_user_id
                metadata['album_cover_image'] = albums_cover_image
            m = copy.deepcopy(metadata)
            yield scrapy.Request(url=sound_url,
                                 meta={"audiodata": m},
                                 callback=self.parse_audio_user,
                                 errback=self.handle_error,
                                 priority=10
                                 )
    def parse_audio_user(self,response):
        metadata = response.meta['audiodata']

        sound_info = json.loads(response.text)
        sound = None
        try:
            sound = sound_info['info']['sound']
        except Exception as e:
            print '---------info   sound'
            print e
        user = None
        try:
            user = sound_info['info']['user']
        except Exception as e:
            print e
        tags = None
        try:
            tags = sound_info['info']['tags']

        except Exception as e:
            print e
        metadata['audio_tags'] = tags
        try:
            metadata['upper_person_url'] = self.host_url + '/' + str(user['id'])
        except Exception as e:
            print e
        try:
            upper_id = self.uid_prefix + str(user['id'])
            metadata['upper_id'] = upper_id
        except Exception as e:
            print e
        try:
            upper_introduce = user['intro']
            upper_introduce = re.sub('<(.*?)>', '', upper_introduce, re.S)
            metadata['upper_introduce'] = upper_introduce
        except Exception as e:
            print e
        try:
            upper_name = user['username']
            metadata['upper_name'] = upper_name
        except Exception  as e:
            print e
        try:
            upper_head_image = user['icon']
            metadata['upper_head_image'] = upper_head_image
        except Exception as e:
            print e
        try:
            audio_create_time = sound['create_time']
            metadata['audio_create_time'] = self.getTime(audio_create_time)
        except Exception as e:
            print e
        try:
            audio_introduce = sound['intro']
            audio_introduce = re.sub('<(.*?)>', '', audio_introduce, re.S)
            metadata['audio_introduce'] = audio_introduce
        except Exception as e:
            print e
        try:
            audio_cover_image = sound['front_cover']
            metadata['audio_cover_image'] = audio_cover_image
        except Exception as e:
            print e
        try:
            metadata['audio_duration'] = int(int(sound['duration'])/1000)
        except Exception as e:
            print e
        try:
            metadata['audio_mp3_url_low'] = self.audio_host + sound['soundurl_32']
        except Exception as e:
            print e

        try:
            metadata['audio_mp3_url_middle'] = self.audio_host + sound['soundurl_64']
        except Exception as e:
            print e
        try:
            metadata['audio_mp3_url_high'] = self.audio_host + sound['soundurl_128']
        except Exception as e:
            print e
        try:
            metadata['audio_id'] = self.uid_prefix + str(sound['id'])
        except Exception as e:
            print e
        try:
            metadata['audio_play_times'] = sound['view_count']
        except Exception as e:
            print e
        try:
            metadata['audio_points'] = sound['point']
        except Exception as e:
            print e
        try:
            metadata['audio_uptimes'] = sound['uptimes']
        except Exception as e:
            print e
        try:
            category_item = sound['breadcrumb']
            category_ids = re.findall('href="(.*?)">', category_item, re.S)
            category_names = re.findall('">(.*?)</a>', category_item, re.S)
            metadata['audio_category_first_id'] = category_ids[0].split('/')[-1]
            metadata['audio_category_last_id'] = category_ids[1].split('/')[-1]
            metadata['audio_category_first_name'] = category_names[0]
            metadata['audio_category_last_name'] = category_names[1]
        except Exception as e:
            print e
        try:
            metadata['audio_name'] = sound['soundstr']
        except Exception as e:
            print e
        try:
            metadata['upper_fansnum'] = user['fansnum']
        except Exception as e:
            print e
        try:
            metadata['upper_soundnum'] = user['soundnum']
        except Exception as e:
            print e

        timestamp = time.time()
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2017-08-28 20:28:54)
        format_date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        item = MzhanItem()
        item['touch_time'] = format_date
        for key, value in metadata.items():
            item[key] = value
        yield item


    @classmethod
    def getTime(cls, timestr):
        try:
            time_local = time.localtime(float(timestr))
            return time.strftime("%Y-%m-%d", time_local)
        except Exception as e:
            print e
            return timestr

    def next_requests(self):

        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        # TODO: Use redis pipeline execution.
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)

            if not data:
                # Queue empty.
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)