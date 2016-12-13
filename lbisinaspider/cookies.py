# coding:utf-8
import base64
import json

import requests

WEIBO_ACCOUNTS = [
    {'username': '452381072@qq.com', 'password': 'liubiaocan771121'}
]


def get_cookies(accounts=None):
    if accounts is None:
        accounts = WEIBO_ACCOUNTS

    login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    cookies = []

    proxies = {
        'http': 'http://dev-proxy.oa.com:8080',
        'https': 'http://dev-proxy.oa.com:8080'
    }

    for item in accounts:
        login_name = base64.b64encode(item['username'].encode('utf-8')).decode('utf-8')

        data = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": login_name,
            "service": "sso",
            "sp": item['password'],
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }

        r = requests.Session()
        result = r.post(login_url, data, proxies=proxies)

        result = json.loads(result.text)

        if result['retcode'] == '0':
            print('account:{0} login successed'.format(item['username']))
            cookie = r.cookies.get_dict()
            cookies.append(cookie)
        else:
            print('account:{0} login failed'.format(item['username']))

    return cookies
