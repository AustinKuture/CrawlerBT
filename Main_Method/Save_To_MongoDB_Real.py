#coding=utf-8
import redis
import datetime
from pymongo import MongoClient


# 远程Redis的数据处理
class RemoteRedis(object):

    # 初始化
    def __init__(self):

        self.remote_redis = redis.Redis(host='127.0.0.1',
                                        port=6379,db=0)

    # 返回远程Redis数据库中所有的key
    def bt_keys(self):

        remote_keys = self.remote_redis.keys()

        return remote_keys

    # 根据key查询相应的value
    def bt_value(self, key):

        value = self.remote_redis.get(key)

        return value

    # 清洗掉Redis数据库中的数据
    def flush_redis_dta(self):

        # print('共清洗缓存数据{}条'.format(self.remote_redis.dbsize()))
        clear_count = self.remote_redis.dbsize()
        self.remote_redis.flushall()

        return clear_count


# Mongodb 数据库操作
class MongoDB_Operator(object):

    # 初始化
    def __init__(self, db, collec):

        mongo_client = MongoClient(host='127.0.0.1',
                                   port=27017)

        self.mongo_collect = mongo_client[db][collec]

        if self.mongo_collect.count({'name': 'kuture_create_database'}) == 0:

            init_result = self.mongo_collect.insert({'name': 'kuture_create_database'})

            print('---初始化数据库',init_result)
            # 添加索引
            try:

                self.mongo_collect.create_index('name', unique=True)
            except Exception as error:

                print('创建索引失败：',error)
            else:

                print('-----创建索引成功！-----')

    # 增
    def mongo_insert(self, jsons):

        self.mongo_collect.insert(jsons)

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

    # 向Mongo数据库中写入数据
    def insert_data_to_mongo(self, bt_key, my_redis):

        current_time = datetime.datetime.now()
        print('{}月{}日 {}:{}:{}--开始写入数据'.format(current_time.month,
                                      current_time.day,
                                      current_time.hour,
                                      current_time.minute,
                                      current_time.second))

        total_count = self.mongo_collect.count()

        repeat_count = 0
        for line in bt_key:

            try:

                line = line.decode('utf-8')
                bt_value = my_redis.bt_value(line).decode()

                line = str(line).replace('.', '*_*')

                mongo_operator.mongo_insert({'name': line, 'magnet': bt_value})
            except Exception as error:

                # print('数据写入错误：',error)
                repeat_count += 1
                continue

        print('{}月{}日 {}:{}:{}--数据写入完成'.format(current_time.month,
                                              current_time.day,
                                              current_time.hour,
                                              current_time.minute,
                                              current_time.second))
        print('新增数据{}条\n重复数据{}条\n清洗缓存数据{}条'.format(self.mongo_collect.count()-total_count,
                                                   repeat_count,
                                                   remote_redis.flush_redis_dta()))




# 远程Redis
remote_redis = RemoteRedis()
bt_keys = remote_redis.bt_keys()

# Mongodb
mongo_operator = MongoDB_Operator('movie_bt', 'jiji_hot_bt')

# 向Mongo数据库中写入数据
mongo_operator.insert_data_to_mongo(bt_keys, remote_redis)

# 清洗掉Redis中的缓存数据























