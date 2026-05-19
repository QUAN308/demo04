import requests
import pandas as pd
from io import StringIO
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"

print("🔄 Đang tải dữ liệu...")
response = requests.get(url, timeout=30, verify=False)
print(f"✓ Status: {response.status_code}")

print("\n📊 Đang phân tích dữ liệu...")
df = pd.read_csv(StringIO(response.text), encoding_errors='ignore')

print(f"\n✓ Tổng hàng: {len(df)}")
print(f"✓ Tổng cột: {len(df.columns)}")
print(f"\n📋 Các cột:\n{df.columns.tolist()}")
print(f"\n📊 Dữ liệu (5 hàng đầu):\n{df.head()}")
