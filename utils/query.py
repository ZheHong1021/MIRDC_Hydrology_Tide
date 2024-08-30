from config.DB import DB
import os
from utils.load_env import load_env
from logs.logger import setup_logger

# 加載 .env 文件中的環境變數
load_env()
# 設定 logger
logger = setup_logger()


class Query:
    def __init__(self):
        # 資料庫連線
        # 如果連接失敗，會回傳 None
        self.connection = DB().connect_db()

    # 尋找站點
    def selectStationID(self, station_id):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                        SELECT * FROM `water_external_measure_station` 
                            WHERE `id` = %s;
                    """, 
                    station_id,
                )
                rows = cursor.fetchall() # 捕捉多的，因為有不確定的可能
                return rows or None
            except Exception as e:
                logger.error(f'⛔ 查詢 [water_external_measure_station]資料庫時發生錯誤: {e}')

 
    # 新增站點
    def insertStation(self, station_id, station_name):
        with self.connection.cursor() as cursor:
            try:
                sql = """
                    INSERT INTO water_external_measure_station 
                    (`id`, `type`, `name`) 
                    VALUES (%s, %s, %s);
                """

                cursor.execute(sql,
                    (station_id, os.environ.get('STATION_TYPE_NAME', 'TideStation'), station_name)
                )

                self.connection.commit()
                return cursor.lastrowid
        
            except Exception as e:
                logger.error(f'⛔ 新增至資料庫中時發生錯誤: {e}')


    # 取得這個站點有數據的measure_time
    def selectTideLevelMeasureTime(self, station_id, year):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                        SELECT `measure_time` FROM `water_external_measure_tide_station_data` 
                            WHERE `station_id` = %s AND YEAR(`measure_time`) = %s;
                    """, 
                    (station_id, year,)
                )
                rows = cursor.fetchall() # 捕捉多的，因為有不確定的可能
                # 取得 measure_time列表(flat)
                return [row['measure_time'] for row in rows] or list()
            except Exception as e:
                logger.error(f'⛔ 查詢 [water_external_measure_tide_station_data]日期資料庫時發生錯誤: {e}')
    

    # 尋找是否有潮高資料
    def selectTideLevel(self, station_id, measure_time):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                        SELECT `id` FROM `water_external_measure_tide_station_data` 
                            WHERE `station_id` = %s AND `measure_time` = %s;
                    """, 
                    (station_id, measure_time),
                )
                rows = cursor.fetchall() # 捕捉多的，因為有不確定的可能
                return rows or None
            except Exception as e:
                logger.error(f'⛔ 查詢 [water_external_measure_tide_station_data]資料庫時發生錯誤: {e}')
    
    # 新增潮高資料
    def insertTideLevel(self, station_id, measure_time, level):
        with self.connection.cursor() as cursor:
            try:
                sql = """
                    INSERT INTO water_external_measure_tide_station_data 
                    (`station_id`, `measure_time`, `level`) 
                    VALUES (%s, %s, %s);
                """

                cursor.execute(sql,
                    (station_id, measure_time, level)
                )

                self.connection.commit()
                return cursor.lastrowid
        
            except Exception as e:
                logger.error(f'⛔ 新增至資料庫中時發生錯誤: {e} ({measure_time} => {level})')

    # 批次新增潮高資料
    def batchInsertTideLevels(self, datas):
        with self.connection.cursor() as cursor:
            try:
                sql = """
                    INSERT INTO water_external_measure_tide_station_data 
                    (`station_id`, `measure_time`, `level`) 
                    VALUES (%s, %s, %s);
                """

                cursor.executemany(sql, datas)

                self.connection.commit()
                return cursor.lastrowid
        
            except Exception as e:
                logger.error(f'⛔ 新增至資料庫中時發生錯誤: {e}')