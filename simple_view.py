import requests
import pandas as pd
from io import BytesIO
import sys
import urllib3

# Thiết lập encoding UTF-8 cho stdout
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"

print("🔄 Đang tải dữ liệu...")
response = requests.get(url, timeout=30, verify=False)
print(f"✓ Status: {response.status_code}\n")

print("📊 Đang phân tích dữ liệu...")
df = pd.read_csv(BytesIO(response.content), encoding='utf-8-sig')

print(f"✓ Tổng hàng: {len(df)}")
print(f"✓ Tổng cột: {len(df.columns)}")

print("\n" + "╔" + "═" * 120 + "╗")
print("║" + " " * 45 + "📊 DỮ LIỆU TỪ API" + " " * 59 + "║")
print("╚" + "═" * 120 + "╝\n")

print("📋 Chi tiết (10 hàng đầu):\n")

if HAS_TABULATE:
    # Chỉ hiển thị 10 hàng đầu
    table_str = tabulate(df.head(10), headers="keys", tablefmt="grid", showindex="always")
    print(table_str)
else:
    print(df.head(10).to_string(index=True))

print("\n" + "═" * 122 + "\n")
