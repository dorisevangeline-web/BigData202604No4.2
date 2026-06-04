# 使用輕量級 Python 映像檔
FROM python:3.9-slim

# 安裝 Chromium 和必要的依賴
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app
COPY . .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 使用 gunicorn 啟動 Flask
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app", "--timeout", "120"]