import pymysql
import os
from utils.load_env import load_env
from logs.logger import setup_logger

# 加載 .env 文件中的環境變數
load_env()

# 設定 logger
logger = setup_logger()


class DB:
    def __init__(self):
        self.host = os.environ.get('DB_HOST', 'localhost')
        self.user = os.environ.get('MYSQL_USER', '')
        self.passwd = os.environ.get('MYSQL_PASSWORD', '')
        self.database = os.environ.get('MYSQL_DATABASE', 'dbname')
        self.port = os.environ.get('DB_PORT', 3306)
    
    def connect_db(self): # 連線資料庫
        try:
            db = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                port=int(self.port),
                cursorclass=pymysql.cursors.DictCursor
            )
            return db
        except Exception as e:
            logger.error('連線資料庫失敗: {}'.format(str(e)))
        return None