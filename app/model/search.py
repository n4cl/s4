# coding: utf8

import requests
from json import dumps
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read("app/model/config.ini")


class ElasticSearchClient(object):

    def __init__(self):
        self.url = "http://" + config.get("elasticsearch", "ip")

    def search_nippo(self, json):
        """ 日報の検索 """
        search_api = self.url + "/es/_search"
        json = dumps(json, encoding='utf-8')
        return self._post_data(search_api, json)

    def analyze_text(self, text):
        """ 文字列に形態素解析を実行する """
        analyze_api = self.url + "/es/_analyze?analyzer=ja_text_analyzer"
        return self._post_data(analyze_api, text)

    def _post_data(self, api, data):
        res = requests.post(api, data=data)
        return res.json()

def main():
    """
    動作テスト
    TODO: テスト書きたい、テストを分離したい
    """
    esc = ElasticSearchClient()

    keyword = "CMS"
    query = {
             "query":{
               "bool":{
                 "must":[
                   {
                     "query_string":{
                       "default_field":"text",
                       "query": keyword,
                     }
                   },
                 ],
                }
              }
            }
    print esc.search_nippo(query)

    text = "日報のデータをダウンロードしました。"
    print esc.analyze_text(text)


if __name__ == '__main__':
    main()
