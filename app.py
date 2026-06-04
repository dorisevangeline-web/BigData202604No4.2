from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import time
import os

app = Flask(__name__)

# ==========================================
# 設定區
# ==========================================
TARGET_STORES = [
    {"name": "全家", "url": "https://www.family.com.tw/Marketing/zh/Event"},
    {"name": "7-11", "url": "https://www.7-11.com.tw/special/newsList.aspx"},
    {"name": "萊爾富", "url": "https://www.hilife.com.tw/events_activity.aspx"}
]

TARGET_KEYWORDS = ["啤酒", "咖啡", "飲料", "冰品", "拿鐵", "美式", "霜淇淋", "第二杯", "買一送一"]
FILTER_KEYWORDS = ["icon", "logo", "arrow", "btn", "button", "footer", "header", "svg", "facebook", "instagram", "line", "app", "download", "cube"]

def create_driver():
    chrome_options = Options()

    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    service = Service(ChromeDriverManager().install())
    
    # 現在這裡就可以正確使用 service 變數了
    driver = webdriver.Chrome(service=service, options=chrome_options)

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def is_valid_event(text, img_url, link):
    combined = (text + img_url + link).lower()
    return any(k.lower() in combined for k in TARGET_KEYWORDS) or \
           any(k in combined for k in ["coffee", "drink", "campaign", "promo", "event", "activity"])

def fetch_all_events(target_store_name=None):
    events_data = []
    driver = create_driver()

    try:
        for store in TARGET_STORES:
            if target_store_name and store["name"] != target_store_name:
                continue
            
            # 使用獨立 try-except 處理單一網站錯誤
            try:
                print(f"\n🌍 正在爬取: {store['name']} ({store['url']})")
                driver.get(store["url"])
                time.sleep(3) 
                
                soup = BeautifulSoup(driver.page_source, "html.parser")
                items = soup.find_all("a")
                
                count = 0
                for item in items:
                    img = item.find("img")
                    if not img: continue
                    
                    img_url = urljoin(store["url"], img.get("src") or img.get("data-src") or "")
                    title = (img.get("alt") or item.get("title") or item.get_text(strip=True) or "").strip()
                    link = urljoin(store["url"], item.get("href", ""))
                    
                    if any(f in img_url.lower() for f in FILTER_KEYWORDS): continue
                    if len(title) < 3: continue
                    
                    if is_valid_event(title, img_url, link):
                        events_data.append({
                            "store": store["name"],
                            "title": title[:40],
                            "img_url": img_url,
                            "link": link
                        })
                        count += 1
                print(f"✅ {store['name']} 爬取成功，共找到 {count} 筆活動")
                
            except Exception as e:
                print(f"❌ {store['name']} 爬取失敗: {str(e)}")
                # 發生錯誤時繼續下一個迴圈
                continue

    finally:
        driver.quit()
    return events_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update')
def update_events():
    target_store = request.args.get('store')
    return jsonify(fetch_all_events(target_store))

if __name__ == '__main__':
    # Render 會自動設定 PORT 環境變數，若沒設定則預設 10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)