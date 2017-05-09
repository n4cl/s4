S4
====

## Usage
configファイルの次の[login_name]と[login_password]に利用するSSSのIDとパスワードを入力する
> vi config
> sss_user=[login_name]
> sss_passwd=[login_password]

#### flask APサーバーの起動方法
> python main.py

起動後、以下のアドレスに対してGETリクエストを行うと、前日分の日報データをjson形式で返す
> http://[server ip address]/sss

