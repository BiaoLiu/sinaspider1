# coding:utf-8
import re

import scrapy
from scrapy import Selector
from scrapy.spider import CrawlSpider

from lbisinaspider.items import UserProfileItem

FOLLOW_URL = 'http://weibo.cn/{0}/follow'
FANS_URL = 'http://weibo.cn/{0}/fans'
PROFILE_URL = 'http://weibo.cn/{0}/profile?filter=1&page=1'

# 获取微博数、关注数、粉丝数
INFOMATION1_URL = 'http://weibo.cn/attgroup/opening?uid={0}'
INFOMATION2_URL = 'http://weibo.cn/{0}/info'

HOME_URL = 'http://weibo.cn/u/{0}'


class SinaSpider(CrawlSpider):
    name = "sina"
    allowed_domains = ['http://weibo.cn']
    start_urls = [
        5235640836, 5676304901, 5871897095, 2139359753, 5579672076, 2517436943, 5778999829, 5780802073, 2159807003,
        1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
        2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
    ]

    def start_requests(self):
        global HOME_URL, FOLLOW_URL, FANS_URL, PROFILE_URL, INFOMATION1_URL

        user_id = self.start_urls.pop()

        INFOMATION1_URL = INFOMATION1_URL.format(user_id)
        # FOLLOW_URL = FOLLOW_URL.format(user_id)
        # FANS_URL = FANS_URL.format(user_id)
        # PROFILE_URL = PROFILE_URL.format(user_id)
        # GROUPS_URL = GROUPS_URL.format(user_id)

        # yield scrapy.Request(url=INFOMATION1_URL, meta={'id': user_id}, callback=self.parser_user_profile1)
        yield scrapy.Request(url=INFOMATION2_URL, meta={'id': user_id}, callback=self.parser_user_profile2)

        # yield scrapy.Request(url=PROFILE_URL, meta={'id': user_id}, callback=self.paser_user_profile)
        # yield scrapy.Request(url=FOLLOW_URL, meta={'id': user_id}, callback=self.paser_follow)
        # yield scrapy.Request(url=FANS_URL, meta={'id': user_id}, callback=self.paser_fans)

    def parser_user_profile1(self, response):
        selector = Selector(response)
        result = selector.xpath("//div[@class='u']/div[@class='tip2']/a/text()").extract()

        user_profile = UserProfileItem()
        result = ','.join(result)
        m = re.search('微博\[(?P<weibo_num>\d+)\],关注\[(?P<follow_num>\d+)\],粉丝\[(?P<fans_num>\d+)\]', result)
        user_profile['weibo_num'] = m.group('weibo_num')
        user_profile['follow_num'] = m.group('follow_num')
        user_profile['fans_num'] = m.group('fans_num')
        user_id = response.meta['id']
        user_profile['user_id'] = user_id

        global INFOMATION2_URL
        INFOMATION2_URL = INFOMATION2_URL.format(user_id)

        yield scrapy.Request(url=INFOMATION2_URL, meta={'item': UserProfileItem}, callback=self.parser_user_profile2)

    def parser_user_profile2(self, response):
        selector = Selector(response)
        result = selector.xpath("//div[@class='tip'][1]/following-sibling::*[1]")
        result2 = selector.xpath("//div[@class='tip' and position()=1]")

        result3=selector.xpath("//div[@class='tip']")

        print(result)

    def paser_follow(self, response):
        pass

    def paser_fans(self, response):
        pass
