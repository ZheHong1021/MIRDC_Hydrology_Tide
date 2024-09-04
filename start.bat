@echo off
REM 執行 auto_crawler.py
python auto_crawler.py
IF %ERRORLEVEL% NEQ 0 (
    echo auto_crawler.py 執行失敗，不執行 app.py
    exit /app 1
)

REM 如果 A.py 成功，執行 app.py
python app.py
IF %ERRORLEVEL% NEQ 0 (
    echo app.py 執行失敗
    exit /app 1
)

echo auto_crawler.py 和 app.py 都執行成功