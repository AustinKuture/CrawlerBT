# coding=utf-8
import requests
import json


class Doubai:
    def __init__(self):  # 初始化url

        self.__url_temp = [{'url': 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count=18&loc_id=108288',
                          'referer': 'https://m.douban.com/movie/nowintheater'}]

        self.__headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'}

    # 请求数据，返回响应
    def __url_list(self, request_url, referer):

        print(request_url)

        self.__headers.update({'Referer': referer})
        r = requests.get(request_url,
                         headers=self.__headers)

        return r.content.decode()

    def __post_html_shuju(self, html_str):

        r = json.loads(html_str)
        dict_title = []
        url_dict = []
        ret = r["subject_collection_items"]
        for i in ret:
            dict_title.append(i['title'])
            url_dict.append(i['url'])

        return (dict_title, url_dict)

    def run(self):

        url_st = self.__url_temp[0]

        num = 0
        while True:

            request_url = url_st['url'].format(num)

            print(num)
            print('----->', request_url)

            html_str = self.__url_list(request_url, url_st['referer'])

            with_baocun = self.__post_html_shuju(html_str)

            title, url = with_baocun

            guo = ""
            for i in range(len(title)):

                guo += title[i] + '--' + url[i] + '\n'

            print(guo)

            try:
                with open('haha.txt', 'a') as f:
                    f.write(guo)
                f.close()
            except Exception as erro:
                print(erro)
                continue

            if len(with_baocun[0]) < 18:

                break
            num += 18


if __name__ == '__main__':

    d = Doubai()
    d.run()