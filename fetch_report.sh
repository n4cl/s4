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
wget -q --no-check-certificate --load-cookies cookies.txt -O page_report --post-data "cmd=schgrpweek&sid=0&nid=0&date=$year$month$day&bpage=schgrpweek&gid=10&bdate=$year$month$day&row=0&dspknd=0&uid=50&seldate=$year$month$day" https://3s.kksnet.co.jp/cgi-bin/sss/s3.cgi

# ==================================
# NOTE: SSSのCSVデータはユニークな値を持たず更新処理が行えないため次の方法は行わない
# 検索クエリーをなげるとCSVが生成される仕組み
#wget --no-check-certificate --load-cookies cookies.txt -O page_query  --post-data="_location=s3search.cgi%3Fcmd%3Dsearchlists&_locationsame=s3search.cgi%3Fcmd%3Dsearchcdnback%26smode%3D1&cmd=searchcmdcdn&kind=U&_submit=%B8%A1%BA%F7&hstartyear=2017&hstartmonth=01&hstartday=19&hendyear=2017&hendmonth=01&hendday=19&nstartyear=0000&nstartmonth=00&nstartday=00&nendyear=0000&nendmonth=00&nendday=00&jstartyear=0000&jstartmonth=00&jstartday=00&jendyear=0000&jendmonth=00&jendday=00&memo=&hmid=&srid=" "https://3s.kksnet.co.jp/cgi-bin/sss/s3search.cgi" 
#
# 日報の詳細を取得
#wget --no-check-certificate --load-cookies cookies.txt -O report.csv  "https://3s.kksnet.co.jp/cgi-bin/sss/s3search.cgi/searchdtlnippo.csv?cmd=searchlistdtlexport&sort=-1&filename=searchdtlnippo.csv"
# ==================================

