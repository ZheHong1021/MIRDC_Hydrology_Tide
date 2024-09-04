# 計算函數執行時間的裝飾器
def print_exec_time(func):
    import time
    def warp(*args, **kwargs):
        start_time = time.time() # 開始時間
        function_name = func.__name__ # 函數名稱
        result = func(*args, **kwargs)

        # 計算執行時間(單位: 秒)
        exec_time = time.time() - start_time
        print(f"Function: {function_name}執行時間: {exec_time:.4f} sec")
        return result
    return warp