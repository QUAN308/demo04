import requests
import pandas as pd
from io import StringIO, BytesIO
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"

print("🔄 Đang tải dữ liệu...")
response = requests.get(url, timeout=30, verify=False)
print(f"✓ Status: {response.status_code}\n")

# Thử nhiều encoding khác nhau
encodings = ['utf-8-sig', 'utf-8', 'big5', 'gb2312', 'cp950', 'latin-1']

for enc in encodings:
    try:
        print(f"🔍 Thử encoding: {enc}")
        df = pd.read_csv(BytesIO(response.content), encoding=enc)
        print(f"   ✓ Thành công!\n")
        
        # Xóa BOM nếu có
        if df.columns[0].startswith('ï»¿'):
            df.columns = [col.replace('ï»¿', '') for col in df.columns]
        
        print(f"   Tổng hàng: {len(df)}")
        print(f"   Tổng cột: {len(df.columns)}")
        print(f"   Cột đầu: {df.columns[0]}")
        print(f"   \n   Dữ liệu (2 hàng đầu):\n{df.head(2)}\n")
        print("=" * 100)
        break
        
    except Exception as e:
        print(f"   ✗ Lỗi: {str(e)[:50]}\n")
