#/bin/bash
set -eu

# sssのログインに利用するユーザー/パスワードをロードする
source ./config

# 昨日の日付を取得
# TODO: 引数で取得日付を変更できるようにする
#d=$(date +"%Y%m%d")
d=$(date -d '1 day ago' +"%Y%m%d")
year="${d:0:4}"
month="${d:4:2}"
day="${d:6:2}"

# ログインのためのクッキー更新
wget -q --no-check-certificate --keep-session-cookies --save-cookies=cookies.txt -O page_cokkie --post-data "cmd=logincmd&UserID=$sss_user&_word=$sss_passwd&_submit=ログイン" https://3s.kksnet.co.jp/cgi-bin/sss/s3.cgi 

# 前日のデータを取得している
wget -q --no-check-certificate --load-cookies cookies.txt -O - --post-data "cmd=schgrpweek&sid=0&nid=0&date=$year$month$day&bpage=schgrpweek&gid=10&bdate=$year$month$day&row=0&dspknd=0&uid=50&seldate=$year$month$day" https://3s.kksnet.co.jp/cgi-bin/sss/s3.cgi

