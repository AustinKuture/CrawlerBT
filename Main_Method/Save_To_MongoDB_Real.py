#coding=utf-8
import redis
import json
from threading import Thread,Lock
from pymongo import MongoClient
#from Read_Remote_Redis import RemoteRedis


# 远程Redis的数据处理
class RemoteRedis(object):

    # 初始化
    def __init__(self):

        #self.__remote_host = 'GdV6XFgGqXG%hv'
        #self.__remote_pwd = 'Yin#bIXN%'
        self.remote_redis = redis.Redis(host='127.0.0.1',
                                port=6379,
                                   db=0,
                                   )

    # 返回远程Redis数据库中所有的key
    def bt_keys(self):

        remote_keys = self.remote_redis.keys()

        return remote_keys


    # 根据key查询相应的value
    def bt_value(self, key):

        value = self.remote_redis.get(key)

        return value


# Mongodb 数据库操作
class MongoDB_Operator(object):

    total_num = None

    # 初始化
    def __init__(self, db, collec):

        mongo_client = MongoClient(host='127.0.0.1',
                                   port=27017)

        self.mongo_collect = mongo_client[db][collec]

        self.total_num = self.mongo_collect.count()

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

    # 去重线程
    def __thd_mongo_remove_repeat(self, thd_lock):

        for line in self.mongo_collect.distinct('name'):

            try:

                reapt_num = self.mongo_collect.count({'name': line})
                for remove_name in range(1, reapt_num):

                    print('--->删除',line)
                    thd_lock.acquire()
                    self.mongo_collect.remove({'name': line}, 0)
                    thd_lock.release()

            except Exception as error:

                print('删除时出现错误：', error)
                continue

    # 去重
    def mongo_remove_repeat(self):

        print('开始去重，当前数量为：',self.mongo_collect.count())

        thd_list = []
        thd_lock = Lock()

        # 开启线程进行批量去重
        for thd_start in range(5):

            try:
                thd = Thread(target=self.__thd_mongo_remove_repeat,
                             args=(thd_lock,))
                thd.start()
            except Exception as error:

                print('线程错误：',error)
                continue
            else:

                thd_list.append(thd)

        for thd_end in thd_list:

            thd_end.join()

        print('去重结束，当前数量为：', self.mongo_collect.count())


# 远程Redis
remote_redis = RemoteRedis()
bt_keys = remote_redis.bt_keys()

# Mongodb
mongo_operator = MongoDB_Operator('movie_bt', 'jiji_hot_bt')

# 向Mongo数据库中写入数据
for line in bt_keys:

    line = line.decode('utf-8')
    bt_value = remote_redis.bt_value(line).decode()

    line = str(line).replace('.', '*_*')

    mongo_operator.mongo_insert({'name':line,'unique':True,'magnet':bt_value})


# 去重
mongo_operator.mongo_remove_repeat()























