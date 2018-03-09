import redis
import logging
from maga import Maga
from urllib import parse


logging.basicConfig(level=logging.INFO)

class Crawlers(Maga):

    async def handler(self, infohash, addr):

        logging.info(infohash)

# 节点爬取
crawler = Crawlers()
datas = crawler.run(6881)

print(datas)






































