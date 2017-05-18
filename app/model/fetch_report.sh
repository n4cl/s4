#/bin/bash
# 指定した日付の日報グループを取得する
# YYYYMMDDで引数を与える
set -eu

# sssのログインに利用するユーザー/パスワードをロードする
source ./config

# 引数で入力した日付を取得
d=$1
year="${d:0:4}"
month="${d:4:2}"
day="${d:6:2}"

# ログインのためのクッキー更新
wget -q --no-check-certificate --keep-session-cookies --save-cookies=cookies.txt -O page_cokkie --post-data "cmd=logincmd&UserID=$sss_user&_word=$sss_passwd&_submit=ログイン" https://3s.kksnet.co.jp/cgi-bin/sss/s3.cgi 

# 前日のデータを取得している
wget -q --no-check-certificate --load-cookies cookies.txt -O - --post-data "cmd=schgrpweek&sid=0&nid=0&date=$year$month$day&bpage=schgrpweek&gid=10&bdate=$year$month$day&row=0&dspknd=0&uid=50&seldate=$year$month$day" https://3s.kksnet.co.jp/cgi-bin/sss/s3.cgi

