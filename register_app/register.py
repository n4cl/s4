# coding: utf-8

import sys
import requests
from json import dumps
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read("config.ini")


class S3Client(object):

    def __init__(self):
        # REST API のエンドポイント
        self._endpoint = "http://" + config.get("server", "ap_server") + "/sss/report"

    def search(self, keyword):
        # リクエストのクエリパラメータ
        p = {"date": keyword}
        return self._request(self._endpoint, p)

    def _request(self, uri, params):
        # HTTP
        _res = requests.get(uri, params=params)
        return _res.json()


class ESClient(object):
    nid = None

    def __init__(self):
        # REST API のエンドポイント
        self._endpoint = "http://" + config.get("server", "es_server") + "/es/report"

    def add_document(self, json):
        uri = self._endpoint + "/" + json["nid"]
        self.nid = json["nid"]
        del json["nid"]
        json = dumps(json, encoding='utf-8')
        return self._request(uri, json)

    def _request(self, uri, params):
        _res = requests.put(uri, data=params)
        return _res.json()
         
if __name__ == '__main__':
    client = S3Client()
    response = client.search(sys.argv[1])
    for res in response["report"]:
        esc = ESClient()
        r = esc.add_document(res)
        print r, esc.nid
