# coding:utf-8
import re

import scrapy
from scrapy import Selector
from scrapy.spider import CrawlSpider, Spider

from lbisinaspider.items import UserProfileItem, WeiboItem

FOLLOW_URL = 'http://weibo.cn/{0}/follow'
FANS_URL = 'http://weibo.cn/{0}/fans'

POSTED_WEIBO_URL = 'http://weibo.cn/{0}/profile?filter=1&page=1'

# 获取微博数、关注数、粉丝数
INFOMATION1_URL = 'http://weibo.cn/attgroup/opening?uid={0}'
INFOMATION2_URL = 'http://weibo.cn/{0}/info'

HOME_URL = 'http://weibo.cn/u/{0}'


class SinaSpider(Spider):
    name = "sina"
    allowed_domains = ['http://weibo.cn']
    delay = 2
    # start_urls = [
    #     5235640836, 5676304901, 5871897095, 2139359753, 5579672076, 2517436943, 5778999829, 5780802073, 2159807003,
    #     1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
    #     2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
    # ]

    start_urls = [
        5235640836, 5676304901
    ]

    # def start_request(self):
    #     return scrapy.Request(url='https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)',callback=self.post_login)


    def start_requests(self):
        global HOME_URL, FOLLOW_URL, FANS_URL, POSTED_WEIBO_URL, INFOMATION1_URL
        while len(self.start_urls) > 0:
            user_id = self.start_urls.pop()

            infomation1_url = INFOMATION1_URL.format(user_id)
            posted_weibo_url = POSTED_WEIBO_URL.format(user_id)
            follow_url = FOLLOW_URL.format(user_id)
            fans_url = FANS_URL.format(user_id)

            # yield scrapy.Request(url=infomation1_url, meta={'id': user_id}, callback=self.parser_user_profile1)
            yield scrapy.Request(url=posted_weibo_url, meta={'id': user_id}, callback=self.parser_posted_weibo)

            # yield scrapy.Request(url=follow_url, meta={'id': user_id}, callback=self.parser_follow)
            # yield scrapy.Request(url=fans_url, meta={'id': user_id}, callback=self.parser_fans)

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

        global INFOMATION2_URL, FANS_URL
        infomation2_url = INFOMATION2_URL.format(user_id)

        yield scrapy.Request(url=infomation2_url, meta={'item': user_profile}, callback=self.parser_user_profile2,
                             dont_filter=True)

    def parser_user_profile2(self, response):
        selector = Selector(response)
        result = selector.xpath("//div[@class='tip'][1]/following::*[1]/text()").extract()

        user_profile = response.meta['item']

        # result = selector.xpath("//div[@class='tip'][1]/following-sibling::*[1]")
        # result2 = selector.xpath("//div[@class='tip'][position()=1]")
        # result3 = selector.xpath("//div[@class='tip']")

        result = ','.join(result)

        m1 = re.search('昵称:(\S+?),', result)
        m2 = re.search('性别:(\S+?),', result)
        m3 = re.search('地区:(\S+?),', result)
        m4 = re.search('生日:(\S+?),', result)
        m5 = re.search('性取向:(\S+?),', result)
        m6 = re.search('婚姻状况:(\S+?),', result)
        m7 = re.search('个性签名:(\S+?),', result)

        user_profile['nickname'] = m1.group(1)
        user_profile['gender'] = m2.group(1)
        user_profile['city'] = m3.group(1) if m3 else ''
        user_profile['birthday'] = m4.group(1) if m4  else ''
        user_profile['sex_orientation'] = m5.group(1) if m5 else ''
        user_profile['marriage'] = m6.group(1) if m6 else ''
        user_profile['signature'] = m7.group(1) if m7 else ''

        yield user_profile

    def parser_posted_weibo(self, response):
        selector = Selector(response)

        result = selector.xpath("//div[@class='c' and @id]")
        for item in result:
            weibo = WeiboItem()
            weibo['content'] = item.xpath("div/span[@class='ctt']/text()").extract_first()
            weibo_data = item.xpath("div/a/text()").extract()
            weibo_data = ','.join(weibo_data)

            m = re.search('赞/[(\w+)/],转发/[(\w+)/],评论/[(\w+)/]', weibo_data)
            weibo['like_num'] = m.group(1)
            weibo['share_num'] = m.group(2)
            weibo['comment_num'] = m.group(3)

            

    def parser_follow(self, response):
        pass

    def parser_fans(self, response):
        id = response.meta.get('id', 'empty')
        print(id)
        user_profile = UserProfileItem()
        user_profile['user_id'] = id

        yield user_profile
