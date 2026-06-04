# 使用 Python 3.11
FROM python:3.11-slim

# 安裝 Chrome 和系統依賴 (這一段是關鍵！)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有檔案
COPY . .

# 設定環境變數
ENV PORT=10000

# 使用 Gunicorn 啟動 (這是穩定的生產模式)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app", "--timeout", "120"]