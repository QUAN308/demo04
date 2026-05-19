import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"

try:
    print(f"🔄 Kiểm tra URL: {url}")
    print("Đang gửi request...")
    
    response = requests.get(url, timeout=10, verify=False)
    print(f"✓ Trạng thái: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
    print(f"Content-Length: {len(response.content)} bytes")
    
    # Hiển thị 500 byte đầu tiên
    print(f"\n📄 Dữ liệu (500 byte đầu):\n{response.text[:500]}")
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
