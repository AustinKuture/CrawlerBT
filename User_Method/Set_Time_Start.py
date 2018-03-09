import time
import datetime
from Main_Method.BT_URL import HotSearch, SearchBT

def do_some_thing():

    print('开始执行任务')

    # 获取热门词汇
    hot_words = HotSearch('')
    hot_list = hot_words.hot_search_word()

    for words in hot_list:
        SearchBT(words).bt_search_run()

    print('任务执行结束，进行下一办计时')

def set_time_start(h=0, m=0, s=0):

    while True:

        while True:

            nows = datetime.datetime.now()

            print('当前时间：时{}-分{}-秒{}'.format(nows.hour, nows.minute, nows.second))
            if nows.hour == h:break

            time.sleep(5*60)
        do_some_thing()

set_time_start(h=3)