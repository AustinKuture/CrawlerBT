#coding=utf-8

import redis
from base64 import b85decode


# 远程Redis的数据处理
class RemoteRedis(object):

    # 初始化
    def __init__(self):

        self.__remote_host = 'GdV6XFgGqXG%hv'
        self.__remote_pwd = 'Yin#bIXN%'
        self.remote_redis = redis.Redis(host=b85decode(self.__remote_host).decode(),
                                   port=6379,
                                   db=0,
                                   password=b85decode(self.__remote_pwd).decode())

    # 返回远程Redis数据库中所有的key
    def bt_keys(self):

        remote_keys = self.remote_redis.keys()

        return remote_keys


    # 根据key查询相应的value
    def bt_value(self, key):

        value = self.remote_redis.get(key)

        return value










































