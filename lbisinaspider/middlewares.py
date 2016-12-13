# coding:utf-8
import random
from .cookies import get_cookies


class ProxyMiddleware:
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://dev-proxy.oa.com:8080'


class CookieMiddleware:
    def process_request(self, request, spider):
        request.cookies = random.choice(get_cookies())
