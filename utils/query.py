from config.DB import DB
class Query:
    def __init__(self):
        # 資料庫連線
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
                print(f'⛔ 查詢 [water_external_measure_station]資料庫時發生錯誤: {e}')

 
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
                    (station_id, "Tide", station_name)
                )

                self.connection.commit()
                return cursor.lastrowid
        
            except Exception as e:
                print(f' ⛔ 新增至資料庫中時發生錯誤: {e}')
    

    # 尋找是否有潮高資料
    def selectTideLevel(self, station_id, measure_time):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                        SELECT * FROM `water_external_measure_tide_level` 
                            WHERE `station_id` = %s AND `measure_time` = %s;
                    """, 
                    (station_id, measure_time),
                )
                rows = cursor.fetchall() # 捕捉多的，因為有不確定的可能
                return rows or None
            except Exception as e:
                print(f'⛔ 查詢 [water_external_measure_tide_level]資料庫時發生錯誤: {e}')
    
    # 新增潮高資料
    def insertTideLevel(self, station_id, measure_time, level):
        with self.connection.cursor() as cursor:
            try:
                sql = """
                    INSERT INTO water_external_measure_tide_level 
                    (`station_id`, `measure_time`, `level`) 
                    VALUES (%s, %s, %s);
                """

                cursor.execute(sql,
                    (station_id, measure_time, level)
                )

                self.connection.commit()
                return cursor.lastrowid
        
            except Exception as e:
                print(f'⛔ 新增至資料庫中時發生錯誤: {e} ({measure_time} => {level})')