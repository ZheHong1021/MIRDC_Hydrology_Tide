import os
from utils.load_env import load_env
from utils.load_stations import load_stations
from alive_progress import alive_bar
from logs.logger import setup_logger
from core.Station import Station

# 設定 logger
logger = setup_logger()


if __name__ == "__main__":
    # 載入環境變數
    load_env()

    # 取得所有站點資訊(HASH MAP)
    # {"舊": "新"}
    stations_hash_map = load_stations()

    # 檔案目錄路徑
    FOLDER = 'save/csv'
    FOLDER_PATH = os.path.join(os.getcwd(), FOLDER)

    # 得到該目錄下所有檔案名稱
    FILENAMES = os.listdir(FOLDER_PATH)
    

    # 一一讀取個檔案資訊
    with alive_bar(len(FILENAMES)) as bar:
        for index, filename in enumerate(FILENAMES):
            # 檔案路徑
            PATH = os.path.join(FOLDER_PATH, filename)

            # 取得該PATH的basename但不要副檔名
            BASENAME = os.path.splitext(os.path.basename(PATH))[0]

            print("-----------------------------------------")
            print(f'📁 {index+1}/{len(FILENAMES)} {BASENAME}')

            # 站點物件
            station = Station(PATH)

            # 檢查檔案名稱並且加入路徑(不通過就跳過)
            if not station.check_filename_and_add_path():
                continue

            # 切割檔案名稱取得變數
            station.split_filename_to_get_parameter()

            # 取得或新增新站點的資訊(ID、name)
            if not station.get_or_create_new_station_information(stations_hash_map):
                continue

            # 解析CSV報表 => 回傳DataFrame
            df = station.parse_csv_report()

            # 將 dataframe中的數據進行寫入到資料庫
            station.write_dataframe_to_database(df)

            bar()