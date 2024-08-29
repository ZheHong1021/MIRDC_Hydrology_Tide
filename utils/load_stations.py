import json
import os

def load_stations():
    # 獲取當前檔案所在目錄的路徑
    current_directory = os.path.dirname(__file__)

    # 獲取上一層目錄的路徑
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))

    # 得到json檔案的路徑
    to_path = os.path.join(parent_directory, 'json', 'stations.json')

    with open(to_path, mode='r', encoding='utf8') as f:
        json_data = json.load(f) # 讀取 json中的資料
        return json_data