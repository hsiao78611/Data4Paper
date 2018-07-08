# Data4Paper
some kickstarter crawlers and data preprocessing notebooks.


* crawl_ 開頭的，都是各個爬蟲的主程式，大概只負責紀錄、輸入、輸出。

packages 中：
* utils 放的大多比較像是工具的東西，很多是從其他人那複製及修改的。
* explore 爬 KS 上全部成功專案的連結。（df 表示 DataFrame，input 是 BS 解析過的 html；output 是一個 DataFrame 形態的表格）
* creator 爬募資人的 about、created、backed。（comments 沒有用到，錯誤應該很多）
* individuals 爬個別專案的 project（主頁）、rewards、faqs、updates、comments。（其中有兩個 crawler，upd 開頭的抓的是個別 update 的內容，因為比較單純就沒有另外開個 df 開頭的檔案）

我是有做出可以透過 Tor 去偽裝成其他 IP，但有時候會比較慢，或中斷。
結果 Kickstarter 好像也沒在管，之後抓我都關掉沒用了...
另外，為了能夠同時抓上萬筆專案的資料，尤其是資助者留言的部分，
所以我也有利用 multiprocessing，實現最多同時 8 組 crawler 在跑。

dataPrep 中有整理過後的前處理過程，若 GitHub 無法順利展示 *.ipynb 內容，請至以下網址觀看畫面擷取內容。

[https://drive.google.com/drive/folders/18vJ-7h3uAnj1Nz-JwQMBfK2a1x7nkRsN?usp=sharing](https://drive.google.com/drive/folders/18vJ-7h3uAnj1Nz-JwQMBfK2a1x7nkRsN?usp=sharing)
