# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.utils.project import get_project_settings

from lbisinaspider.items import UserProfileItem, WeiboItem


class LbisinaspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class SinaPipeline(object):
    def __init__(self):
        self.db_settings = get_project_settings().get('DATABASES')

        self.db = pymysql.connect(host=self.db_settings['HOST'],
                                  port=self.db_settings['PORT'],
                                  db=self.db_settings['NAME'],
                                  user=self.db_settings['USER'],
                                  password=self.db_settings['PASSWORD'],
                                  charset='utf8')

    def process_item(self, item, spider):
        cursor = self.db.cursor()

        if isinstance(item, UserProfileItem):
            user_id = str(item['user_id'])
            nickname = item['nickname']
            gender = item['gender']
            city = item['city']
            birthday = item['birthday']
            marriage = item['marriage']
            signature = item['signature']
            weibo_num = int(item['weibo_num'])
            follow_num = int(item['follow_num'])
            fans_num = int(item['fans_num'])

            try:
                sql = 'insert into s_user values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, (
                    user_id,
                    nickname,
                    gender,
                    city,
                    birthday,
                    marriage,
                    signature,
                    weibo_num,
                    follow_num,
                    fans_num
                ))
                self.db.commit()
            except Exception as e:
                self.db.rollback()

        elif isinstance(item, WeiboItem):
            weibo_id = item['weibo_id']
            user_id = item['user_id']
            content = item['content']
            like_num = item['like_num']
            comment_num = item['comment_num']
            share_num = item['share_num']
            pub_time = item['pub_time']
            pub_client = item['pub_client']

            try:
                sql = 'insert into s_post_weibo values(%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, (
                    weibo_id,
                    user_id,
                    content,
                    like_num,
                    comment_num,
                    share_num,
                    pub_time,
                    pub_client
                ))
                self.db.commit()
            except Exception as e:
                self.db.rollback()
