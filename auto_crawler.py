import requests
import zipfile
import os
import random
import time
from utils.load_stations import load_stations
from alive_progress import alive_bar
from logs.logger import setup_logger
from datetime import datetime


# 設定 logger
logger = setup_logger()

class Crawler:
    def __init__(self, station_id, year, station_name):
        self.station_fullname = f"{year}_{station_id}_{station_name}_tide"

        # 指定保存壓縮檔案的路徑
        self.zip_file_path = "save/zip/saved_file.zip"

        # 指定解壓縮後的目標資料夾
        self.extract_to_path = "save/csv/"

        # 爬蟲連結
        self.url = "https://ocean.cwa.gov.tw/V2/data_interface/download/download_file"

        # 爬蟲帶入參數
        self.params = {
            "dataset": "Tide-his", # 資料集名稱
            "factor": "t",
            "download_type": "csv", # 下載檔案的格式
            "begin": year, # 起始年份
            "end": year, # 結束年份
            "station_id": station_id, # 站號
        }

        
    # 將壓縮檔下載下來
    def download(self):
        # 透過request + stream將檔案下載下來
        response = requests.get(self.url, params=self.params, stream=True)

        # 檢查請求是否成功
        if response.status_code == 200:

            # 開啟檔案，並寫入從請求中取得的內容
            with open(self.zip_file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            logger.info(f"📥 [{self.station_fullname}]壓縮檔下載成功，檔案已下載到: {self.zip_file_path}")

        else:
            logger.error(f"⛔ 下載失敗，請確認是否有該站點ID: {self.station_fullname}")
    
    # 解壓縮
    def extract(self):
        # 檢查目標資料夾是否存在，不存在則創建
        if not os.path.exists(self.extract_to_path):
            os.makedirs(self.extract_to_path)

        try:
            # 使用 zipfile 解壓縮
            with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_to_path)
            
            logger.info(f"✅ [{self.station_fullname}]壓縮成功 (路徑: {self.extract_to_path})")
        except Exception as e:
            logger.error(f"⛔ 解壓縮失敗: {e}")


if __name__ == "__main__":
    # 站點列表
    stations_hash_map = load_stations()

    # 取得今年年份
    year = datetime.now().year

    # 隨機等待時間
    sleep_time = random.randint(2, 8)
    
    with alive_bar(len(stations_hash_map)) as bar:
        for station_id, value in stations_hash_map.items():
            # 站點名稱
            station_name = value.get("name", None)

            # 創建爬蟲物件
            crawler = Crawler(station_id, year, station_name)

            # 下載壓縮檔案
            crawler.download()

            # 將壓縮檔解壓成csv檔
            crawler.extract()


            # 等待隨機時間
            time.sleep(sleep_time)

            bar()