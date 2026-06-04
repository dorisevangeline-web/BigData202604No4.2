FROM python:3.11-slim

# 安裝系統編譯依賴與 Chrome
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 確保先安裝 pip 的升級版，這能解決很多安裝套件時的雜訊
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=10000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]