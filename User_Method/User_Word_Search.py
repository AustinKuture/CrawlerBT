#coding=utf-8
from Main_Method.BT_URL import SearchBT

user_search_words = None
try:

    with open('./User_Method/user_words.txt', 'r') as rf:

        user_search_words = rf.readlines()
except Exception as error:

    print(error)


for hot_words in user_search_words:

    print(hot_words)

    user_search = SearchBT(hot_words)
    user_search.bt_search_run()


