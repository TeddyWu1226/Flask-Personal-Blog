# Flask-Personal-Blog
利用Flask結合Python其他功能實現個人部落格

本專案使用模板來源:https://startbootstrap.com/theme/clean-blog 其html、圖片、CSS、JS檔案均修改於網址內提供之檔案。

一、專案介紹:

本專案主要設計為五頁-主頁、部落格頁、個人資料頁、登入頁、文章頁

1.主頁(爬蟲)：內容主要執行爬蟲工作，爬取本人github上專案資訊與介紹，並每次讀取頁面時就更新資料。

2.部落格頁(SQL):讀取儲存於SQL內文章列表資訊並回傳，使用者可藉由上方按鈕進行排版顯示方便找尋，以及登入後可進行「新增、編輯、隱藏、刪除」文章之動作。

※github專案列表與文章列表皆透過Django template tags語法-迴圈與判定式顯示，詳情可點選index.html與post.html的頁面參考網頁原始碼。

3.個人資料頁(靜態):純靜態HTML寫法，介紹個人資料。

4.登入頁(讀取本地檔案or檔案內使用者列表):可進行登入判定，修改登入狀態。

※本專案採用單一使用者狀態判定，雖然可建立多組帳號密碼，但同時間只能有一個使用者登入，否則會衝突使用。

5.文章頁(SQL):點選進文章後顯示的頁面，有獨立性ID可個別顯示、並設阻擋使用者透過修改網址讀取隱藏文章。

預覽圖如下:

![blogpic](https://user-images.githubusercontent.com/103618758/191594946-5bd272e1-abd5-4a38-a3e3-9dbfdd89e0f2.jpg)

二、文章操作介紹(登入後)

設計懸浮動態視窗，方便使用者登入後進行新增、編輯等動作，

![blogpost](https://user-images.githubusercontent.com/103618758/191596387-0964fb5a-09d3-4a5b-980f-eaeb7bb3885a.jpg)

以及設有隱藏及刪除按鈕方便隱藏文章或刪除文章。

![blogart](https://user-images.githubusercontent.com/103618758/191596486-f231e3a1-288b-4abd-8723-bf4e77d256aa.jpg)
