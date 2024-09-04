import os
from core.Report import Report
from utils.query import Query
from utils.decorators import print_exec_time
from logs.logger import setup_logger

# 設定 logger
logger = setup_logger()

class Station:
    def __init__(self, path):
        self.path = path # 檔案路徑
        self.year = None # 該檔案年份
        self.old_station_id = None # 舊站點ID
        self.station_id = None # 新站點ID
        self.station_name = None # 新站點名稱

        self.query = Query() # Query物件
    
    # 檢查檔案名稱並且加入路徑
    def check_filename_and_add_path(self):

        # 得到該PATH的副檔名
        EXTENSION = os.path.splitext(self.path)[-1]

        # 如果副檔名不是.csv就跳過
        if EXTENSION != '.csv':
            return False

        return True

    # 切割檔案名稱取得變數
    def split_filename_to_get_parameter(self):
        # 取得該PATH的basename但不要副檔名
        BASENAME = os.path.splitext(os.path.basename(self.path))[0]

        # 切割變數
        # ● year: 年份
        # ● old_station_id: 舊站點ID
        # ● station_name: 站點名稱
        # ● type: 站點類型
        self.year, self.old_station_id, self.station_name, self.type = BASENAME.split('_')
    
    # 取得或新增新站點的資訊(ID、name)
    def get_or_create_new_station_information(self, stations_hash_map):
        # 先檢查是否有該站點ID
        station = stations_hash_map.get(str(self.old_station_id), None)
        if station is None:
            logger.error(f"⛔ 找不到站點ID: {self.old_station_id}，請確認json檔案中是否有該站點ID")
            return False

        # 如果有該站點ID，則取得新站點ID、name
        self.station_id = station.get('id', None)
        self.station_name = station.get('name', None)


        # 確定該站點是否存在於資料庫中
        is_exist_station = self.query.selectStationID(self.station_id)
        
        # 如果該站點不存在於資料庫中，則需要去進行新增
        if not is_exist_station:
            self.query.insertStation(self.station_id, self.station_name)
            logger.info(f'✅ 新增站點ID: {self.station_id} 成功')

        return True
    
    
    # 將csv報表中的數據進行解析
    @print_exec_time
    def parse_csv_report(self):
        # 創建一個Report物件
        report = Report(self.path)

        # 擷取該CSV報表的內容
        report.fetch_report()

        # 添加datetime欄位
        report.add_measure_time_column()

        # 轉換nan為None
        report.transfer_nan_to_none()

        # 取得該報表的DataFrame並回傳
        return report.df

    
    # 將 dataframe中的數據進行寫入到資料庫
    @print_exec_time
    def write_dataframe_to_database(self, df):
        # 取得這個站點有數據的measure_time
        # 改用 set 來提高查詢效率
        measure_times = set(self.query.selectTideLevelMeasureTime(self.station_id, self.year))

        # 新增的數據(batch)
        create_datas = list()

        # 取得潮高欄位
        LEVEL_COLUMN = os.environ.get('LEVEL_COLUMN', ':00')

        # 開始進行資料庫寫入
        for _, row in df.iterrows():

            # 取得潮高
            level = row[LEVEL_COLUMN] 
                
            # 取得時間
            measure_time = row['measure_time']

            # 確定該時間是否已經存在於資料庫中
            if measure_time in measure_times:
                continue # 存在就不用繼續了


            # 儲存要新增的數據
            create_datas.append((self.station_id, measure_time, level))

        # 如果有新增的數據
        if create_datas:
            self.query.batchInsertTideLevels(create_datas)
            logger.info(f'✅ [{self.station_id} - {self.station_name}]新增 {len(create_datas)} 筆潮高資料成功')
