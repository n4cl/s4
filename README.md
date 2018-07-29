S4
====

desknet's SSSの検索拡張システムで下記の3点から構成されている
- クローラーサーバー
- 検索エンジン(Elasticsearch)
- 検索拡張(Chrome拡張)

## 要件
- Python 2.7
- Elasticsearch 5.4
- desknet's SSS V3.0J R1

## 準備

### Pythonモジュール
```
必要なモジュールをインストール
pip install -r requirements.txt
```

### Elasticsearch plugins
```
index作成時に必要なモジュールをインストール
bin/elasticsearch-plugin install analysis-icu
bin/elasticsearch-plugin install analysis-kuromoji
```

### Elasticsearchへindexの作成
```
# indexの生成
curl -X PUT -d @elastic/report.json http:/[Elasticsearch IP or Name]/es
```

### desknet's SSS クローラー設定
ルートディレクトのconfigファイルの次の[login_name]と[login_password]に利用するSSSのIDとパスワードを入力する
```
sss_user=[login_name]
sss_passwd=[login_password]
```

## 起動方法
### クローラーサーバーの起動方法
```
# サーバー起動
python main.py
```
```
# 下記アドレスに対してGETリクエストを行うと、前日分の日報データをjson形式で返す
http://[Crawler server ip address]/sss/report

# パラメータに日付を付与すろと、指定日の日報データをjsonで返す
http://[Crawler server ip address]/sss/report?date=20180701
```

## Elasticsearchへの登録方法
register_app内のregister.pyから登録することが可能
```
# register_app内のconfig.iniの以下を入力
[server]
ap_server = application_server_ip    # Crawler servcer のIP+Port
es_server = elasticsearch_server_ip  # Elasticserch ServerのIP+Port
```

```
# 2018年7月28日の日報をElasticsearchへ登録する
python register.py 20180728
```

## SSSでの検索方法
- chromeExtenstionフォルダ内の検索拡張ツールをGoogleChromeに追加する
- SSSの検索画面に拡張検索ボタンが追加される
![検索画面](https://user-images.githubusercontent.com/5583062/43363183-d9e949dc-9339-11e8-88e0-c5a975d3d7f8.png)
