# 捕捉歷史潮汐數據

## 環境設定
### 虛擬環境+套件安裝
1. 安裝Python虛擬環境的套件 **(如果已經安裝不用操作)**
```shell=
pip install virtualenv
```

2. 建立Python的虛擬環境 **(記得要在該專案目錄下執行)**
```shell=
py -m venv venv
```
3. 進入虛擬環境
```shell=
.\venv\Scripts\activate
```
4. 安裝 requirements.txt的套件
```shell=
pip install -r requirements.txt
```

### 資料庫設定
1. 首先將 .env.example這個檔案進行複製為另一個檔案，並改名為 .env
```shell=
copy .env.example .env
```
2. 修改.env
```shell=
# MySQL settings
MYSQL_DATABASE=DATABASE # 資料庫名稱
MYSQL_USER=USER # 資料庫帳號
MYSQL_PASSWORD=PASSWORD # 資料庫密碼
DB_HOST=localhost
DB_PORT=3306
```


---

## 檔案目錄說明
### 目錄
|目錄名稱|說明|
|-|-|
|config|相關設定的程式。EX: 資料庫連線|
|core|主程式中較核心的Class類別|
|database|會使用到的資料表|
|json|儲存捕捉站點的資訊|
|logs|程式執行的日誌|
|save|下載下來的檔案|
|utils|常用的functions|


### 檔案
|檔案名稱|說明|
|-|-|
|.env.example|環境設定變數|
|app.py|將下載下來的csv進行資料解析並儲存到資料庫中|
|auto_crawler.py|將海象資料下載下來並且進行壓縮儲存到save目錄中|
|requirements.txt|使用到的Python Package|
|start.bat|一鍵執行指令，先執行auto_crawler.py，再執行app.py|

---

## 資料來源
[海象環境資訊平台 - 海象資料下載](https://ocean.cwa.gov.tw/V2/data_interface/download?dataset=Tide-his&title=%E6%BD%AE%E4%BD%8D%E7%AB%99%E8%A7%80%E6%B8%AC%E6%AD%B7%E5%8F%B2%E8%B3%87%E6%96%99&format=CSV&all_formats=TXT,CSV&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhc2V0SUQiOiIxNDEiLCJ0IjoxNzI0OTgwODY3fQ.edYS2-29eQkX7DiBfl7FTpQxcVz4Xm9SyL4lKQbx10o)


## 捕捉方式
將下載的csv檔案放置到『csv』目錄下，記得要先進行解壓縮，這樣程式才能捕捉到這些檔案進行資料擷取。


## 站點資訊
目前會透過捕捉到的csv檔案名稱判斷該檔案的資訊。

【檔案名稱 - 2024_1166_東石潮位站_tide】
* 年份：2024
* 站點代號：1166
* 站點名稱：東石潮位站
* 站點類型：tide

由於站點代號目前捕捉下來的會是舊版代號，之後中央氣象局可能會全面改用新版代號，因此資料庫部分將會儲存為新版站點代號，為了儲存新版代號，會透過下面列出的JSON將代號進行改變。

<br>


### 取得新站點代號
[中央氣象署海象觀測站列表	]([oceanapi.cwa.gov.tw](https://oceanapi.cwa.gov.tw/restapi/v2/static/station/station_info.html))
透過點擊上方的連結即可導引到站點資訊說明的網站了

<br>

### 目前儲存的站點
* json/stations.json
```json=
{
    "1166": {
        "id": "C4L02",
        "name": "東石潮位站"
    },
    "1186": {
        "id": "C4Q02",
        "name": "東港潮位站"
    },
    "1176": {
        "id": "C4N01",
        "name": "將軍潮位站"
    },
    "1486": {
        "id": "C4P01",
        "name": "高雄潮位站"
    }
}
```


### 新增捕捉代號
目前捕捉的站點只有上方四個站點，如果日後需要新增更多站點的話，只需要在 json/stations.json進行新增即。

【新增範例】
```json=
{
    "1166": {
        "id": "C4L02",
        "name": "東石潮位站"
    },
    "1186": {
        "id": "C4Q02",
        "name": "東港潮位站"
    },
    "1176": {
        "id": "C4N01",
        "name": "將軍潮位站"
    },
    "1486": {
        "id": "C4P01",
        "name": "高雄潮位站"
    },
	"舊版ID": {
		"id": "新版ID",
		"name": "被新增的潮位站"
	}
}
```

