import redis
import urllib.parse as parse

local_redis = redis.Redis(host='127.0.0.1', port=6379, db=0)

all_keys = local_redis.keys()

for bt_key in all_keys:

    bt_key = bt_key.decode('utf-8')
    bt_str = '\n{}\n'.format(parse.unquote(local_redis.get(bt_key).decode('utf-8')))
    try:

        with open('./User_Method/user_magnet_bt.txt', 'a') as sf:

            sf.write(bt_str)
    except Exception as error:

        print(error)
        continue
    else:

        print(bt_str)
    finally:

        sf.close()











