# coding: utf-8

import sys
import requests
from json import dumps


class S3Client(object):

    def __init__(self):
        # REST API のエンドポイント
        self._endpoint = "http://10.20.30.150:5000/sss/report"

    def search(self, keyword):
        # リクエストのクエリパラメータ
        p = {"date": keyword}
        return self._request(self._endpoint, p)

    def _request(self, uri, params):
        # HTTP 
        res = requests.get(uri, params=params)
        return res.json()

class ESClient(object):
    nid = None
    def __init__(self):
        # REST API のエンドポイント
        self._endpoint = "http://10.20.30.149:9200/es/report"

    def add_document(self, json):
        uri = self._endpoint + "/" + json["nid"]
        self.nid = json["nid"]
        del json["nid"]
        #json = dumps(json, encoding='utf-8', ensure_ascii=False)
        json = dumps(json, encoding='utf-8')
        return self._request(uri, json)

    def _request(self, uri, params):
        res = requests.put(uri, data=params)
        return res.json()
         
if __name__ == '__main__':
    client = S3Client()
    response = client.search(sys.argv[1])
    for res in response["report"]:
        esc = ESClient()
        r = esc.add_document(res)
        print r, esc.nid

