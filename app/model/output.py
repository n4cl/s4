# coding: utf8

from bs4 import BeautifulSoup


def wget_sss_group():
    """
    SSSのグループ表示ページのダウンロード
    Args:
    Returns:
        True: bool: ダウンロード成功
        False: bool: ダウンロード失敗
    """
    from subprocess import Popen, PIPE

    # 非シェル経由でRSYNC実行
    p = Popen(["bash", "./app/model/fetch_report.sh"]
              , stdin = PIPE
              , stdout = PIPE
              , stderr = PIPE)

    # 戻り値が0であれば正常終了
    if p.wait() == 0:
        return True
    else:
        print "SSSページダウンロード中にエラーが発生しました:\n" + str(p.stderr.readlines()[0])
        return False

def wget_sss_nippo(nippo_query):
    """
    日報ページのダウンロード
    Args:
    Returns:
        True: bool: ダウンロード成功
        False: bool: ダウンロード失敗
    """
    from subprocess import Popen, PIPE

    # 非シェル経由でRSYNC実行
    p = Popen(["bash", "fetch_daily_report.sh", nippo_query]
              , stdin = PIPE
              , stdout = PIPE
              , stderr = PIPE)

    # 戻り値が0であれば正常終了
    if p.wait() == 0:
        return p.stdout.read()
    else:
        print "日報ページダウンロード中にエラーが発生しました:\n" + str(p.stderr.readlines())
        return ""

def read_file(file_path):
    """ 
    euc_jisx0213でエンコードされたファイルの読み込み
    Args:
        file_path: str: 読み込むファイルパス
    Return:
        読み込んだ文字列
    """
    from codecs import open
    body = None
    try:
        file = open(file_path, "r", "euc_jisx0213")
        #file = open(file_path, "r", "euc-jp")
        # このネストで失敗することはあるのか 念のため例外処理を追記した
        try:
            body = file.read()
        except IOError as e:
            raise e
        finally:
            file.close()
    except IOError as e:
        raise e
    return body

def extract_nippo(html):
    """ 日報データを取得するためのクエリ部を抽出する """
    nippo = []
    bs = BeautifulSoup(html, "lxml")

    for link in bs.find_all("a"):
        if "nippodetailview" in link.get("href"):
            # クエリ部だけ抜き出す
            nippo.append(link.get("href").split("?")[1])

    return nippo

class sss(object):
    """
    ElasticSearchに登録する日報データオブジェクト

    date: 報告日付
    department: 所属課
    user_name: 報告者名
    text: 報告内容
    """
    bs = None

    report_id = None
    url = None

    template = None
    date = None
    department = None
    user_name = None
    client = None
    other = None
    job = None
    work_class = None
    text = None
    actual_time = None

    # TODO: これどうにかしたい。
    division = {u"tech": u"☆☆☆　システム技術部　日報　☆☆☆"}

    def __init__(self, html):
        self.html = html

    def extract_repot(self):
        self.bs = BeautifulSoup(self.html, "lxml")
        __template = self.__get_template(self.bs)
        self.template = __template

        # TODO: 日報にHTMLタグ埋め込まれるとずれる
        if __template == self.division[u"tech"]:
            self.__get_not_login_report()
        elif not __template:
            #raise
            # TODO: エラーにする予定
            pass


    def __get_template(self, __bs):
        """ 
        日報のテンプレートの種類を取得する
            TODO: 現状システム技術部のみ
        """

        try:
            __bs = __bs.find_all("form")[1]
            __table_tag = __bs.find_all("table")
    
            # メニューバーに変更を加えるボタンが存在するのか
            __l = len(__table_tag[0].find_all("input"))
    
            if __l > 0:
                # 自分の日報の可能性高し
                return 
    
            if __table_tag[3].find_all("font")[1].string == self.division["tech"]:
                return __table_tag[3].find_all("font")[1].string
        except:
            pass

        # 面倒なので、とりあえずNoneを返す
        return None

       
    def __get_not_login_report(self):
        """
        ログインユーザー外の日報HTMLから日報データを抽出する
        """
        self.bs = self.bs.find_all("form")[1]
        table_tag = self.bs.find_all("table")

        __t = table_tag[0].find_all("td")
        # 日付
        self.date = __t[1].string
        # 所属課
        self.department = __t[5].string.strip()
        # 報告者名
        self.user_name = __t[7].string

        __t = table_tag[1].find_all("td")
        # 顧客
        self.client = __t[1].string
        # その他 (顧客)
        self.other = __t[5].string
        # 商品名
        self.job = __t[13].string

        __t = table_tag[3].find_all("font")

        # テンプレート名
        self.template = __t[1].string

        # 区分
        self.work_class = __t[6].string

        # 報告内容
        self.text = table_tag[3].textarea.string

        # 実働時間
        self.actual_time = table_tag[3].find("input")["value"]

def main():
    wget_sss_group()
    # fetch_sss_data()

def fetch_sss_data():
    # 日報のURLを含んだページをダウンロード
    #wget_sss_group()
    """
    file_path = "page_report"
    html = read_file(file_path)
    nippo_query = extract_nippo(html)

    for query in nippo_query:
        print wget_sss_nippo(query).decode("euc_jisx0213")
        #print sss(wget_sss_nippo(query).decode("euc_jisx0213"))
    """
    reports = []
    html = read_file("test")
    #html = read_file("test_myself")
    report = sss(html)

    # TODO: レポートの種類を判定する処理が必要
    # TODO: 自分のときは、別のスクレイピング手段を用意する必要がある
    # idとかclassが全くないので頑張ってスクレイピングする
    try:
        report.extract_repot()
    except:
        pass
#        continue

    reports.append(report)

    json_data = {u"report":[]}
    for r in reports:
        d = {u"data": report.date,
             u"department": report.department,
             u"user_name": report.user_name,
             u"client": report.client,
             u"other": report.other,
             u"job": report.job,
             u"work_class": report.work_class,
             u"test": report.text,
             u"actual_time": report.actual_time}

        json_data[u"report"].append(d)

    from json import dumps
    return dumps(json_data)


if __name__ == '__main__':
    main()

