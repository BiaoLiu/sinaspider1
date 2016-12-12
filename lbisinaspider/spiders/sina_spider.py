# coding:utf-8

import scrapy
from scrapy.spider import CrawlSpider

FOLLOW_URL = 'http://weibo.cn/{0}/follow'
FANS_URL = 'http://weibo.cn/{0}/fans'
PROFILE_URL = 'http://weibo.cn/{0}/profile?filter=1&page=1'
GROUPS_URL = 'http://weibo.cn/attgroup/opening?uid={0}'


class SinaSpider(CrawlSpider):
    name = "sina"
    host = "http://weibo.cn"
    start_urls = [
        5235640836, 5676304901, 5871897095, 2139359753, 5579672076, 2517436943, 5778999829, 5780802073, 2159807003,
        1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
        2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
    ]

    start_userids = set(start_urls)

    def start_requests(self):
        global FOLLOW_URL, FANS_URL, PROFILE_URL, GROUPS_URL
        while True:
            user_id = self.start_userids.pop()

            FOLLOW_URL = FOLLOW_URL.format(user_id)
            FANS_URL = FANS_URL.format(user_id)
            PROFILE_URL=PROFILE_URL.format(user_id)
            GROUPS_URL=GROUPS_URL.format(user_id)

            yield scrapy.Request(url=FOLLOW_URL,)