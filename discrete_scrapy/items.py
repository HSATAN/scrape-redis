# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MzhanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()


    upper_id = scrapy.Field()  # upper 主id
    upper_name = scrapy.Field()  # upper 昵称
    upper_head_image = scrapy.Field()  # upper 头像
    upper_introduce = scrapy.Field()  # upper 介绍
    upper_person_url = scrapy.Field()  # 个人信息主页
    upper_fansnum = scrapy.Field()  # upper 粉丝数目，粉丝数目多的可能内容质量好
    upper_soundnum = scrapy.Field()  # upper 拥有的音频数
    #  这个两个属性可以做推荐用

    audio_id = scrapy.Field()  # 音频id
    audio_name = scrapy.Field()  # 音频标题
    audio_cover_image = scrapy.Field()  # 音频封面
    audio_introduce = scrapy.Field()  # 音频介绍
    audio_tags = scrapy.Field()  # 音频标签
    audio_category_first_name = scrapy.Field()  # 音频所属的主类别
    audio_category_first_id = scrapy.Field()  # 音频所属的主类别id
    audio_category_last_name = scrapy.Field()  # 音频所属的子类别
    audio_category_last_id = scrapy.Field()  # 音频所属的子类别
    audio_duration = scrapy.Field()  # 音频时长
    audio_main_url = scrapy.Field()  # 获取音频页面的url
    audio_play_times = scrapy.Field()  # 播放次数
    audio_uptimes = scrapy.Field()  # 点赞次数,标记喜欢
    audio_points = scrapy.Field()  # 投食次数
    #  这几个属性做推荐的时候可能会用上
    audio_mp3_url_low = scrapy.Field()  # 低音质
    audio_mp3_url_middle = scrapy.Field()  # 中音质
    audio_mp3_url_high = scrapy.Field()  # 高音质
    audio_create_time = scrapy.Field()  # 音频的创建或上传时间

    album_name = scrapy.Field()  # 专辑标题
    album_id = scrapy.Field()  # 专辑id
    album_cover_image = scrapy.Field()  # 专辑封面
    album_create_time = scrapy.Field()  # 专辑创建时间
    album_update_time = scrapy.Field()  # 专辑更新时间
    album_create_user_id = scrapy.Field()  # 专辑的创建者id 根据这个id就可以找到对应的用户信息

    touch_time = scrapy.Field()  # 数据的爬取时间


