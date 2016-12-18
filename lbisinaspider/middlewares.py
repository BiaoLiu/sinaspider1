# coding:utf-8
import random
from .cookies import get_cookies
from .user_agents import user_agents


class ProxyMiddleware:
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(user_agents)
        # request.meta['proxy'] = 'http://dev-proxy.oa.com:8080'


class CookieMiddleware:
    def process_request(self, request, spider):
        request.cookies = get_cookies()
