#/bin/bash
# 日報データを標準出力する
set -eu
source config

# TODO: ファイルは保存しない、つどページの読み込みを行った方が良い
wget -O - -q --no-check-certificate --load-cookies cookies.txt "https://$domain/cgi-bin/sss/s3.cgi?$1" 

