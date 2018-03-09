#coding=utf-8

from maga import Maga
import logging
logging.basicConfig(level=logging.INFO)

class Crawler(Maga):

    async def handler(self, infohash, addr):

        logging.info(infohash)
        print(infohash)
        print(addr)


dht_crawler = Crawler()
dht_crawler.run(6881)