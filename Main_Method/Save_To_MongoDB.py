#coding=utf-8
import json
from pymongo import MongoClient
from User_Method.Read_Remote_Redis import RemoteRedis


class MongoDB_Operator(object):

    # 初始化
    def __init__(self, db, collec):
        mongo_client = MongoClient(host='127.0.0.1',
                                   port=27017)

        self.mongo_collect = mongo_client[db][collec]

    # 增
    def mongo_insert(self, jsons):

        self.mongo_collect.insert(jsons)

        print('数据插入完成-----{}'.format(jsons))

    # 删
    def mongo_delete(self, jsons):
        delete_ret = self.mongo_collect.delete_one(jsons)
        print('id:{}---{}'.format(delete_ret, jsons))

    # 改
    def mongo_correct(self, old, news):
        update_ret = self.mongo_collect.update(old, news)
        print('id:{}---{}'.format(update_ret, news))

    # 查
    def mongo_query(self, jsons):
        query = self.mongo_collect.find(jsons)

        for line in query:
            print(line)


# 远程Redis
remote_redis = RemoteRedis()
bt_keys = remote_redis.bt_keys()

# Mongodb
mongo_operator = MongoDB_Operator('movie_bt', 'jiji_hot_bt')

for line in bt_keys:

    line = line.decode('utf-8')
    bt_value = remote_redis.bt_value(line).decode()

    line = str(line).replace('.', '*_*')

    try:

        mongo_operator.mongo_insert({{'name':line,'unique':True},{'magnet':bt_value}})

    except Exception as error:

        print(error)




























