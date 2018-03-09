#coding=utf-8

import json
import time
import redis
import socket
import random
import base64
import requests
import datetime
from lxml import etree
from urllib import parse
from http import cookiejar
from threading import Thread
from multiprocessing import Process
import urllib.request as urlrequest


user_agents = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; MyIE2; .NET CLR 1.1.4322) ",
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; MyIE2; Maxthon; .NET CLR 1.1.4322) ",
               "Mozilla/5.0 (Windows; U; Windows NT 5.2; rv:1.7.3) Gecko/20041001 Firefox/0.10.1 ",
               "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0 ",
               "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8b) Gecko/20050212 Firefox/1.0+ (MOOX M3) ",
               "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; WOW64; Trident/4.0; uZardWeb/1.0; Server_USA) ",
               "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; WOW64; Trident/4.0; uZardWeb/1.0; Server_KO_KTF) ",
               "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; WOW64; Trident/4.0; uZard/1.0; Server_KO_SKT) ",
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; WOW64; SV1; uZardWeb/1.0; Server_HK) ",
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; WOW64; SV1; uZardWeb/1.0; Server_EN) ",
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; WOW64; SV1; uZardWeb/1.0; Server_CN) ",
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; uZardWeb/1.0; Server_JP) ",
               "Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7 ",
               "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.813.0 Safari/535.1 ",
               "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.794.0 Safari/535.1 ",
               "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1 ",
               "Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 ",
               "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30 ",
               "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.17 (KHTML, like Gecko) Chrome/11.0.652.0 Safari/534.17 ",
               "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10 ",
               "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.15) Gecko/20101027 Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10 "]

local_redis = redis.Redis(host='127.0.0.1',port=6379, db=0)

# 请求验证并获取cookie
class ScanCookies(object):

    def _mycookies(self, secrets, agents):

        try:
            # 创建cookiejar
            mycookiejar = cookiejar.CookieJar()
            # 创建cookie处理器
            handlers = urlrequest.HTTPCookieProcessor(mycookiejar)
            # 创建opener并加入请求头
            opener = urlrequest.build_opener(handlers)
            opener.addheaders = [('User-Agent', agents)]
            # 初次请求获取cookie
            myrequest = urlrequest.Request(secrets)
            opener.open(myrequest,timeout=2)

            cookie_str = ''
            for items in mycookiejar:
                cookie_str = items.name + '=' + items.value

        except Exception as error:

            print(error)

            return
        else:

            return cookie_str


# 搜索BT
class SearchBT(ScanCookies):

    # 初始化
    def __init__(self, search_name):

        self.__ie_type = 'utf-8'

        self.__search_name = search_name
        self.__cookie_name = parse.urlencode({'s':search_name}).replace('s=', '')
        self.__bt_url = 'XmoUNIxjDGcXuvoX=-U=bS`6WZ7*tRYH2TfeJ^``FEB4KE@*UZYy'
        self.__hot_url = 'XmoUNIxjDGcXuvoX=-U=bS`6WZ7*nVbaO6fbZu+'

    # 获取数据
    def _bt_obtain(self, url_type, page_num=0):

        content = ''
        try:

            # 随机代理
            user_agent = random.choice(user_agents)

            redis_cookies = None
            try:

                redis_cookies = local_redis.get('Bt_Cookies')
            except Exception as error:

                print(error)
            else:

                if redis_cookies is None:

                    # 获取cookie信息
                    try:

                        if url_type is 'search':

                            mycookie = self._mycookies(
                                base64.b85decode(self.__bt_url.encode(self.__ie_type)).decode(self.__ie_type).format(
                                    self.__cookie_name,page_num),user_agent)
                        else:

                            mycookie = self._mycookies(
                                base64.b85decode(self.__hot_url.encode(self.__ie_type)).decode(self.__ie_type), user_agent)
                        print(mycookie)
                    except Exception as error:

                        print('***>',error)
                    else:

                        local_redis.set('Bt_Cookies', mycookie)

                headers = {'User-Agent': user_agent,
                           'Cookie': redis_cookies}

                # print(headers)
                # 响应请求

                if url_type is 'search':

                    response = requests.get(
                        base64.b85decode(self.__bt_url.encode(self.__ie_type)).decode(self.__ie_type).format(
                            self.__search_name,page_num),
                                        headers=headers,
                                        timeout=5)
                else:

                    response = requests.get(
                        base64.b85decode(self.__hot_url.encode(self.__ie_type)).decode(self.__ie_type),
                        headers=headers,
                        timeout=5)

                # print(response.url)
                content = response.content.decode('utf-8')
        except Exception as error:

            print('--->',error)
            local_redis.delete('Bt_Cookies')
            return
        else:

            return content

    # 为所有的页码开启线程
    def __obtain_url_data(self, page_num):

        try:

            web_data = etree.HTML(self._bt_obtain('search', page_num))
            bt_url = web_data.xpath('.//div[@class="sbar"]/span/a/@href')
        except Exception as error:

            print('--',error)
        else:

            # 将获取到时的链接放到时队列中
            for line in bt_url:

                try:

                    # 截取种子的名称并进行转码
                    redis_key = parse.unquote(line[str(line).index('dn='):]).replace('dn=','')
                    local_redis.set(redis_key, parse.unquote(line))
                except Exception as error:

                    print(error)
                    continue
                else:

                    print('{}\t{}'.format(redis_key,parse.unquote(line)))
                    # self.__wirte_user_words_bt('./User_Method/user_magnet_bt_url.txt',line)

    # 写入用户指定单词
    def __wirte_user_words_bt(self, file_name, bt_url):

        bt_url = parse.unquote(bt_url) + '\n'

        try:

            with open(file_name, 'a') as sf:

                sf.write(bt_url)
                sf.close()
        except Exception as error:

            print(error)

    # 使用xpath获取url
    def bt_search_run(self):

        thd_list = []

        for p_num in range(1,2):

            thd_get_bt_url = Thread(target=self.__obtain_url_data, args=(p_num,))
            thd_get_bt_url.start()
            thd_list.append(thd_get_bt_url)

        for thd_end in thd_list:

            thd_end.join()

        # print('获取完成')


# 热门搜索
class HotSearch(SearchBT):

    # 每日调频搜索词
    def hot_search_word(self):

        today_hot_words = []
        try:

            web_data = etree.HTML(self._bt_obtain('hot'))
            bt_url = web_data.xpath('.//div[@class="fh"]/a/text()')

            for hot_words in bt_url:

                # print('--------------',hot_words)
                today_hot_words.append(hot_words)
        except Exception as error:

            print('Hotsearch:{}'.format(error))
            return

        else:

            return today_hot_words


if __name__ == '__main__':

    # 获取热门词汇
    hot_words = HotSearch('')
    hot_list = hot_words.hot_search_word()

    for words in hot_list:

        SearchBT(words).bt_search_run()

