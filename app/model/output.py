# coding: utf8

from bs4 import BeautifulSoup

def fetch_group_report(input_date=None):

    from json import dumps
    from datetime import datetime, date, timedelta

    # TODO:引数であるdateは、YYYYMMDDのときしか受け付けない状態
    #      あとでバリエーション増やしてもいいかも
    if input_date:
        # unicode type to str type
        input_date = str(input_date)
        # TODO: 最低限の入力検証...
        if len(input_date) != 8:
            return dumps({"respons": "1", "text": "invalid string length"})
        try:
            date(int(input_date[:4]), int(input_date[4:6]), int(input_date[6:8]))
        except:
            return dumps({"respons": "1", "text": "invalid date format"})
    else:
        input_date = (datetime.now() + timedelta(days=-1)).strftime("%Y%m%d")
    # グループ日報ページから日報のリンク(クエリ部)を取得
    _g = fetch_nippo_link(input_date)
    link = extract_nippo(_g, input_date)
    res = []

    # 各日報からデータをスクレピング
    for query in link:
        html = fetch_report(query)
        d = fetch_sss_data(html)
        d[u"query"] = query

        # ユニークidの取得
        import re
        p = r"nid\=(.*?)\&"
        nid = re.search(p, query).group(1)
        d[u"nid"] = nid
        res.append(d)

    # TODO: 良いレスポンスを考える
    # respons: 0 -> 正常
    #          1 -> 異常
    if res:
        d = {"respons": "0", "report": res}
    else:
        d = {"respons": "1"}

    return dumps(d, encoding='utf-8', ensure_ascii=False)

def fetch_nippo_link(_input_date):
    """
    SSSのグループ表示ページのダウンロード
    Args:
    Returns:
        True: bool: ダウンロード成功
        False: bool: ダウンロード失敗
    """
    from subprocess import Popen, PIPE

    # 非シェル経由でRSYNC実行
    p = Popen(["bash", "./app/model/fetch_report.sh", _input_date]
              , stdin = PIPE
              , stdout = PIPE
              , stderr = PIPE)

    # 戻り値が0であれば正常終了
    if p.wait() == 0:
        return p.stdout.read()
    else:
        print "SSSページダウンロード中にエラーが発生しました:\n" + str(p.stderr.readlines()[0])
        return ""

def fetch_report(nippo_query):
    """
    日報ページのダウンロード
    Args:
    Returns:
        True: bool: ダウンロード成功
        False: bool: ダウンロード失敗
    """
    from subprocess import Popen, PIPE

    # 非シェル経由でRSYNC実行
    p = Popen(["bash", "./app/model/fetch_daily_report.sh", nippo_query]
              , stdin = PIPE
              , stdout = PIPE
              , stderr = PIPE)

    # 戻り値が0であれば正常終了
    if p.wait() == 0:
        return p.stdout.read()
    else:
        print "日報ページダウンロード中にエラーが発生しました:\n" + str(p.stderr.readlines())
        return ""

def extract_nippo(html, input_date):
    """ 日報データを取得するためのクエリ部を抽出する """
    nippo = []
    bs = BeautifulSoup(html, "lxml")

    for link in bs.find_all("a"):
        if "nippodetailview" in link.get("href") or "nippomod" in link.get("href"):
            # クエリ部だけ抜き出す
            _l = link.get("href").split("?")[1]

            # 指定の日付のみ
            if "seldate=" + input_date in _l:
                nippo.append(_l)

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
        """
        BeautifulSoupで取り込む時点で自動で文字コードを認識する
        BeautifulSoupの内部では、Unicode型になっている
        """
        self.bs = BeautifulSoup(self.html, "lxml")
        __template = self.__get_template(self.bs)
        self.template = __template

        # TODO: 日報にHTMLタグ埋め込まれるとずれる
        if __template == self.division[u"tech"]:
            self.__get_not_login_report()
        elif __template == "myself":
            self.__get_login_report()
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
                # 自分の日報
                # TODO: 本当はスクレイピング用のアカウント使えるのが良いが
                return "myself" 
    
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


    def __get_login_report(self):
        """
        ログインユーザーの日報HTMLから日報データを抽出する
        TODO: システム技術部の日報前提のメソッド
        """
        # 所属課 TODO: なぜか自分の日報にはないので。。。
        self.department = u"システム技術2課"

        # 報告者名
        __tb = self.bs.find_all("table")[10]
        self.user_name = __tb.find_all("span", attrs={"class": "font_top_login_name"})[0].string[3:]

        __bs_f = self.bs.find_all("form")[1]

        # 日付
        __date = __bs_f.find_all("input", attrs={"name": "seldate"})[0]["value"]
        self.date = __date[:4] + "-" + __date[4:6] + "-" + __date[6:8]

        # 顧客
        __cdealer = __bs_f.find_all("select", attrs={"name": "cdealer"})
        __cdealer = __cdealer[0].find_all("option", attrs={"selected": True})
        if __cdealer:
            self.client = __cdealer[0].string.strip()
        else:
            self.client = None

        # その他 (顧客)
        __cenduser = __bs_f.find_all("select", attrs={"name": "cenduser"})
        __cenduser = __cenduser[0].find_all("option", attrs={"selected": True})

        if __cenduser:
            self.other = __cenduser[0].string.strip()
        else:
            self.other = None

        # 商品名
        # TODO: タグ構造が微妙なので、あとで考える...
        #self.job = __t[13].string

        # TODO: なんで作ったんだっけ？
        ## テンプレート名
        #self.template = __t[1].string

        # 区分
        __fp4 = __bs_f.find_all("select", attrs={"name": "fp4"})
        self.work_class = __fp4[0].find_all("option", attrs={"selected": True})[0].string.strip()

        # 報告内容
        self.text = __bs_f.textarea.string

        # 実働時間
        #self.actual_time = table_tag[3].find("input")["value"]
        __fp11 = __bs_f.find_all("input", attrs={"name": "fp11"})
        self.actual_time = __fp11[0]["value"]

def main():
    print ""

def fetch_sss_data(html):

    report = sss(html)

    # TODO: レポートの種類を判定する処理が必要
    # TODO: 自分のときは、別のスクレイピング手段を用意する必要がある
    # idとかclassが全くないので頑張ってスクレイピングする
    try:
        report.extract_repot()
    except:
        pass

    d = {u"date": report.date,
         u"department": report.department,
         u"user_name": report.user_name,
         u"client": report.client,
         u"other": report.other,
         u"job": report.job,
         u"work_class": report.work_class,
         u"text": report.text,
         u"actual_time": report.actual_time}

    return d 

if __name__ == '__main__':
    main()

