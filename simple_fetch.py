import requests
import json
from urllib.parse import urlparse

def fetch_and_display_data(url):
    """
    Phiên bản đơn giản: chỉ cần requests library
    """
    try:
        print(f"🔄 Đang tải dữ liệu...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        print(f"✓ Thành công! Mã trạng thái: {response.status_code}")
        print(f"Kích thước: {len(response.content)} bytes\n")
        
        # Thử phân tích JSON
        try:
            data = response.json()
            print("📊 Dữ liệu (JSON):")
            print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
            
            # Lưu file
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("\n✓ Đã lưu vào: data.json")
            
        except json.JSONDecodeError:
            # Nếu không phải JSON, hiển thị dạng text
            if response.text:
                print("📄 Dữ liệu (Text):")
                print(response.text[:2000])
                
                # Lưu file
                with open('data.txt', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("\n✓ Đã lưu vào: data.txt")
                
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    url = "https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/9CB7F264-50B3-4E67-9D29-D1A1054488B2/resource/45C57D8B-596B-480E-9D39-B7A608DC4D1B/download"
    fetch_and_display_data(url)
