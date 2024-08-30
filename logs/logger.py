import logging
import os

def setup_logger():
    # 設定 log 檔名(副檔名為 log)
    log_file = os.path.join(os.getcwd(), 'logs', 'app.log') 

    # 設定 logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # 設定 handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 設定 formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 設定 formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 將 handler 加入 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger