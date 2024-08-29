import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.load_env import load_env
import os

# 加載 .env 文件中的環境變數
load_env()

class Report:
    def __init__(self, path):
        self.path = path
        self.header = os.environ.get('HEADER', 20)
        self.df = None
    
    # 擷取該CSV報表的內容
    def fetch_report(self):
        self.df = pd.read_csv(
            self.path,
            header=self.header, # 指定表格中哪一列作為列索引。預設為0，即第一行
        )

        return self.df
    

    # 新增日期與時間欄位
    def add_measure_time_column(self):
        # 轉換為datetime格式
        self.df["measure_time"] = self.df['yyyymmddhh'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d%H'))

        # # 取得日期
        # self.df["date"] = self.df['measure_time'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))

        # # 取得日期
        # self.df["time"] = self.df['measure_time'].apply(lambda x: datetime.strftime(x, '%H:%M:%S'))

    
    # 轉換nan為None
    def transfer_nan_to_none(self):
        self.df = self.df.replace({np.nan: None})