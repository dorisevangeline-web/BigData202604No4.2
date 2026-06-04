# 使用輕量級 Python 映像檔
FROM python:3.11-slim

# 安裝 Chrome 和相關依賴
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製檔案並安裝套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有程式碼
COPY . .

# 設定環境變數
ENV PORT=10000

# 啟動命令
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]