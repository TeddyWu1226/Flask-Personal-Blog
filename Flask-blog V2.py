"""
作者:Cheng Hong,Wu
網頁模板採用:https://startbootstrap.com/theme/clean-blog
"""
from flask import Flask, render_template, request,redirect,url_for
import time
import pymysql as MySQLdb

# 使用個人SQL帳號密碼、資料庫名稱
user = ""
passwd = ""
database= ""
# 資料庫設計為:
# 資料庫名稱:Blog
# 標籤有:
# ID(鎖定),author(作者),Title(標題),Text(內文),Time(純數顯示),visible(0-顯示 1-不顯示)


# 使用個人登入帳號密碼管理庫(dict)
userdata = { "ID":"",
            "PW":""
}

# 單一登入使用者狀態管理
username = None
userStatus = 0

# Flask建立
app = Flask(__name__,static_url_path='/static')
#app.config["DEBUG"] = True   #用於開啟Debug即時更新模式

# 主頁(爬取個人Github資料後顯示於畫面上)
@app.route("/")
def Home():
    def github_Project(url):  # [0][i] 是名稱  [1][i] 是連結   [2]是介紹
        def httpLoad(html):
            contents = ""
            req = httplib.Request(html, data=None,  # 連線
                                  headers={
                                      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}
                                  )
            reponse = httplib.urlopen(req)
            if reponse.code == 200:  # 當連線正常時
                contents = reponse.read().decode("utf-8")
            return contents

        topic_list = []
        href_list = []
        introduction_list = []
        t = httpLoad(url)
        soup = BeautifulSoup(t, 'html.parser')
        box = soup.find("ol")
        a = box.find_all("a")
        for i in a:
            href = i.get("href")
            href = f"https://github.com{href}"
            topic = i.find("span").get("title")
            topic_list.append(topic)
            href_list.append(href)
            soup2 = BeautifulSoup(httpLoad(href), 'html.parser')
            article = soup2.find("article")
            introduction = article.find("p").get_text()
            introduction_list.append(introduction)
        return topic_list, href_list, introduction_list
    git = github_Project("") # 輸入您的Github網址於此

    # 定義爬下來的github專案標籤 方便匯入html用
    class project(object):
        def __init__(self, title, link, introduction):
            self.title = title
            self.link = link
            self.introduction = introduction

    p_List = []
    for i in range(len(git[0])):
        p_List.append(project(git[0][i], git[1][i], git[2][i]))
    gits = p_List
    return render_template('index.html',gits=gits, userStatus=userStatus)

# 回傳至主頁標籤
@app.route("/index")
def index():
    return redirect(url_for('Home'))

# 關於(靜態網站 顯示我的個人資料)
@app.route("/about")
def about():
    return render_template('about.html', userStatus=userStatus)

# 定義文章標籤 方便傳遞至html中使用)
class articleImformation(object):
    def __init__(self, id, author, title, text, time, visible):
        self.id = id
        self.author = author
        self.title = title
        self.text = text
        self.time = time
        self.visible = visible

# 文章部落格
@app.route('/post', methods=['GET', 'POST'])
def post():
    def SQLload(command):
        article_list = []
        # 連接資料庫
        try:
            db = MySQLdb.connect(host="127.0.0.1", user=user, passwd=passwd,
                                 db=database)  # 連線到資料庫 (輸入您的Table)
            cursor = db.cursor()
            cursor.execute(command)  # 取得資料庫
            SQL_list = cursor.fetchall()
        except:
            print("資料庫連線失敗，請聯絡技術人員協助處理")
            SQL_list = []

        for i in SQL_list:
            article_list.append(articleImformation(i[0],i[1],i[2],i[3],i[4],i[5]))
        return article_list
    articleList = SQLload("SELECT * FROM `blog` ORDER BY `blog`.`Time` DESC") # 開啟網頁時先按時間順序讀取文章列表一遍

    # 網頁操作
    if request.method == 'POST':
        # 按鈕判定(判定是哪個按鈕被點擊)
        def PostbtnCheck(string):  # string>>html屬性抓取 name
            if string in list(request.values.keys()):
                return True
            else:
                return False
        # 修改SQL內資料的function
        def SQL_commad(command):
            db = MySQLdb.connect(host="127.0.0.1", user=user, passwd=passwd,
                                 db=database)  # 連線到資料庫 (輸入您的Table)
            cursor = db.cursor()
            cursor.execute(command)
            db.commit()  # 執行匯出更改後資料

        # 轉時間現在型態為純數組合
        def time_to_number():  # 直接匯入純time.time
            t = time.time()
            t = time.localtime(t)
            timeString = time.strftime("%Y-%m-%d %H:%M:%S", t)
            return timeString

        # 新增貼文
        if PostbtnCheck("createNew"):
            title = request.values['a-title']
            text = request.values['a-text']
            Now = time_to_number()
            command = f"INSERT INTO `blog` (`ID`, `author`, `Title`, `Text`, `Time`, `visible`) " \
                      f"VALUES (NULL, '{username}', '{title}', '{text}', '{Now}', '0');"
            SQL_commad(command)
            return redirect(url_for('post'))

        # 刪除貼文
        elif PostbtnCheck("delete"):
            articleNumber = request.form.get("delete")
            command = f"DELETE FROM blog WHERE `blog`.`ID` = {articleNumber}"
            SQL_commad(command)
            return redirect(url_for('post'))

        # 編輯貼文
        elif PostbtnCheck("editarticle"):
            articleNumber = request.values['a-id']
            title = request.values['a-title']
            text = request.values['a-text']
            Now = time_to_number()
            #print(articleNumber)
            #print(title)
            #print(text)
            #print(Now)


            command = f"UPDATE `blog` SET `Title` = '{title}', `Text` = '{text}', `Time` = '{Now}' WHERE `blog`.`ID` = {articleNumber}"
            SQL_commad(command)

            return redirect(url_for('post'))

        # 隱藏/解隱藏
        elif PostbtnCheck("hide"):
            articleNumber = request.form.get("hide")
            command = f"UPDATE `blog` SET `visible` = '1' WHERE `blog`.`ID` = {articleNumber}"
            SQL_commad(command)
            return redirect(url_for('post'))
        elif PostbtnCheck("unhide"):
            articleNumber = request.form.get("unhide")
            command = f"UPDATE `blog` SET `visible` = '0' WHERE `blog`.`ID` = {articleNumber}"
            SQL_commad(command)
            return redirect(url_for('post'))

        # 排序系列
        # 最新
        elif PostbtnCheck("lastest"):
            command = "SELECT * FROM `blog` ORDER BY `blog`.`Time` DESC"
            articleList = SQLload(command)
            return render_template('post.html', user="", articleList=articleList, userStatus=userStatus,username=username)

        # 最舊
        elif PostbtnCheck("oldest"):
            command = "SELECT * FROM `blog` ORDER BY `blog`.`Time` ASC"
            articleList = SQLload(command)
            return render_template('post.html', user="", articleList=articleList, userStatus=userStatus,username=username)

        # 只看我的文章(登入後顯示)
        elif PostbtnCheck("onlyme"):
            command = f"SELECT * FROM `blog` WHERE `author` LIKE '{username}' ORDER BY `Time` DESC"
            articleList = SQLload(command)
            return render_template('post.html', user="", articleList=articleList, userStatus=userStatus,username=username)


    return render_template('post.html', user="", articleList=articleList, userStatus=userStatus,username=username)


# 文章頁面
@app.route('/post/article<int:id>')
def article(id):  # 加入id 獨立化文章網址
    def SQL_find(id):
        # 連接資料庫
        try:
            db = MySQLdb.connect(host="127.0.0.1", user=user, passwd=passwd,
                                 db=database)  # 連線到資料庫 (輸入您的Table)
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM `blog` WHERE `ID` = {int(id)}")  # 取得資料庫
            i = cursor.fetchall()[0]
            article = articleImformation(i[0], i[1], i[2], i[3], i[4], i[5])
        except:
            print("資料庫連線失敗，請聯絡技術人員協助處理")
            article = articleImformation("0", None, "找不到該文章!", "找不到該文章!",None, 1)

        if int(article.visible) == 1:  # 隱藏文章 禁止讀取
            article = articleImformation("0", None, "找不到該文章!", "找不到該文章!", None, 1)

        return article

    article = SQL_find(id) # 文章資料回傳

    return render_template('post/article.html',article=article, userStatus=userStatus)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global userStatus,username
    # 登入使用者密碼判定
    def LoginCertification(username,password):
        # password = pw_create(password)  # 此為個人密碼加密function 因資料庫內密碼已先加密
        if str(username) in userdata["ID"]:
            t = userdata["ID"].index(str(username))
            if str(password) == userdata["PW"][t]:
                return 1
            else:
                return 0
        else:
            return 0

    tip = ""
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        t = LoginCertification(username, password)
        if t == 1:
            userStatus = 1
            return redirect(url_for('post'))
        else:
            tip = "※使用者或密碼錯誤!"

    return render_template('login.html', tips=tip)

# 檢查登入狀態用
@app.route('/login2')
def login2():
    return f"使用者ID:{username}\n使用者狀態:{userStatus}"

# 登出標籤
@app.route('/logout')
def logout():
    global userStatus,username
    userStatus = 0
    username = None
    return redirect(url_for('login'))

if __name__ == '__main__':
    # app.run()  # 內部跑取
    app.run(host='0.0.0.0', port=5000)  # 公開

