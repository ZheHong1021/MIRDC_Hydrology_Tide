import os
from core.Report import Report
from utils.query import Query
from utils.load_env import load_env
from utils.load_stations import load_stations
from alive_progress import alive_bar


if __name__ == "__main__":
    # 載入環境變數
    load_env()

    # 取得所有站點資訊(HASH MAP)
    # {"舊": "新"}
    stations_hash_map = load_stations()

    # 檔案目錄路徑
    FOLDER = 'csv'
    FOLDER_PATH = os.path.join(os.getcwd(), FOLDER)

    # 得到該目錄下所有檔案名稱
    FILENAMES = os.listdir(FOLDER_PATH)
    

    # 一一讀取個檔案資訊
    with alive_bar(len(FILENAMES)) as bar:
        for index, filename in enumerate(FILENAMES):
            PATH = os.path.join(FOLDER_PATH, filename)

            # 得到該PATH的副檔名
            EXTENSION = os.path.splitext(PATH)[-1]

            # 如果副檔名不是.csv就跳過
            if EXTENSION != '.csv':
                continue

            # 創建一個Query物件
            query = Query()
            
            # 取得該PATH的basename但不要副檔名
            BASENAME = os.path.splitext(os.path.basename(PATH))[0]

            print("-----------------------------------------")
            print(f'📁 {index+1}/{len(FILENAMES)} {BASENAME}')

            # 切割變數
            # ● year: 年份
            # ● old_station_id: 舊站點ID
            # ● station_name: 站點名稱
            # ● type: 站點類型
            year, old_station_id, station_name, type = BASENAME.split('_')

            # 取得新的站點ID
            station = stations_hash_map.get(str(old_station_id), None)
            if station is None:
                print(f"⛔ 找不到站點ID: {old_station_id}")
                continue

            station_id = station.get('id', None)
            station_name = station.get('name', None)

            # 確定該站點是否存在於資料庫中
            is_exist_station = query.selectStationID(station_id)
            
            # 如果該站點不存在於資料庫中，則需要去進行新增
            if not is_exist_station:
                query.insertStation(station_id, station_name)
                print(f'✅ 新增站點ID: {station_id} 成功')
            
            # 創建一個Report物件
            report = Report(PATH)

            # 擷取該CSV報表的內容
            report.fetch_report()

            # 添加datetime欄位
            report.add_measure_time_column()

            # 轉換nan為None
            report.transfer_nan_to_none()

            # 取得該報表的DataFrame
            df = report.df


            # 取得這個站點有數據的measure_time
            measure_times = query.selectTideLevelMeasureTime(station_id)
            
            
            # 開始進行資料庫寫入
            for _, row in df.iterrows():

                # 取得潮高
                level = row[os.environ.get('LEVEL_COLUMN', ':00')] 
                    
                # 取得時間
                measure_time = row['measure_time']

                # 確定該時間是否已經存在於資料庫中
                if measure_time in measure_times:
                    continue # 存在就不用繼續了

                # 新增潮高資料
                new_id = query.insertTideLevel(station_id, measure_time, level)
                # if new_id:
                #     print(f'✅ 新增[{station_id}-{station_name}]潮高資料: 成功 =>({new_id})')


            bar()