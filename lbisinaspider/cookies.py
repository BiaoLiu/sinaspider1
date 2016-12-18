# coding:utf-8
import base64
import json
import random

import requests

WEIBO_ACCOUNTS = [
    {'username': '17032589756', 'password': 'cdefgab789'},
    {'username': '17071197344', 'password': 'cdefgab789'},
    # {'username': '17076087437', 'password': 'cdefgab789'},
    {'username': '15302991848', 'password': 'cdefgab789'},
    # {'username': '17099263437', 'password': 'cdefgab789'},
    {'username': '17088921824', 'password': 'cdefgab789'},
    {'username': '17099260948', 'password': 'cdefgab789'},
    {'username': '15658036485', 'password': 'cdefgab789'},
    # {'username': '15658034035', 'password': 'cdefgab789'},
    {'username': '17088921814', 'password': 'cdefgab789'},
    {'username': '17088921478', 'password': 'cdefgab789'},
    {'username': '17099263437', 'password': 'cdefgab789'},
    {'username': '17061131061', 'password': 'cdefgab789'},
]


# WEIBO_ACCOUNTS = [
#     {'username': '17061131061', 'password': 'cdefgab789'},
# ]


def get_cookies():
    login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'

    # proxies = {
    #     'http': 'http://dev-proxy.oa.com:8080',
    #     'https': 'http://dev-proxy.oa.com:8080'
    # }

    proxies = {

    }

    item = random.choice(WEIBO_ACCOUNTS)
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
        return cookie
    else:
        print('account:{0} login failed'.format(item['username']))
        return get_cookies()
