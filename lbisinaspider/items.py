# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LbisinaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserProfileItem(scrapy.Item):
    user_id = scrapy.Field()
    weibo_num = scrapy.Field()
    follow_num = scrapy.Field()
    fans_num = scrapy.Field()

    nickname = scrapy.Field()
    gender = scrapy.Field()
    city = scrapy.Field()
    birthday = scrapy.Field()

    sex_orientation = scrapy.Field()
    marriage = scrapy.Field()
    signature = scrapy.Field()


class WeiboItem(scrapy.Item):
    weibo_id = scrapy.Field()
    content = scrapy.Field()
    like_num = scrapy.Field()
    comment_num = scrapy.Field()
    reshare_num = scrapy.Field()

    tools = scrapy.Field()
    pubtime = scrapy.Field()
