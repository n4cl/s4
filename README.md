S4
====

desknet's SSSの検索拡張システム

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
- analysis-icu
- analysis-kuromoji

### desknet's SSS クローラー設定
configファイルの次の[login_name]と[login_password]に利用するSSSのIDとパスワードを入力する
```
sss_user=[login_name]
sss_passwd=[login_password]
```

## 起動方法
### flask APサーバーの起動方法
```
python main.py
```
起動後、以下のアドレスに対してGETリクエストを行うと、前日分の日報データをjson形式で返す
```
http://[server ip address]/sss
```

## 検索方法
- chromeExtenstionフォルダ内の検索拡張ツールをGoogleChromeに追加する
- SSSの検索画面に拡張検索ボタンが追加される
