import requests
import json
import pandas as pd
from io import StringIO, BytesIO
import os

# Tắt SSL warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_data(url):
    """
    Tải dữ liệu từ URL
    
    Args:
        url (str): URL của API endpoint
        
    Returns:
        Response object hoặc None nếu có lỗi
    """
    try:
        print(f"Đang tải dữ liệu từ: {url}")
        # Thêm verify=False để bỏ qua kiểm tra SSL certificate
        response = requests.get(url, timeout=30, verify=False)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        print(f"Trạng thái: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải dữ liệu: {e}")
        return None

def detect_format(response):
    """
    Phát hiện định dạng dữ liệu từ response
    """
    content_type = response.headers.get('content-type', '')
    print(f"Content-Type: {content_type}")
    return content_type

def parse_data(response):
    """
    Phân tích dữ liệu dựa trên định dạng
    """
    content_type = detect_format(response)
    
    try:
        # Nếu là JSON
        if 'json' in content_type:
            data = response.json()
            print("\n✓ Dữ liệu JSON:")
            print(json.dumps(data[:100] if isinstance(data, list) else data, 
                           ensure_ascii=False, indent=2))
            return data
        
        # Nếu là CSV
        elif 'text/csv' in content_type or 'csv' in content_type:
            df = pd.read_csv(StringIO(response.text))
            print("\n✓ Dữ liệu CSV:")
            print(df.head())
            print(f"\nShape: {df.shape} (hàng, cột)")
            return df
        
        # Nếu là Excel
        elif 'spreadsheet' in content_type or 'excel' in content_type:
            df = pd.read_excel(BytesIO(response.content))
            print("\n✓ Dữ liệu Excel:")
            print(df.head())
            print(f"\nShape: {df.shape} (hàng, cột)")
            return df
        
        # Nếu là plain text
        elif 'text' in content_type:
            print("\n✓ Dữ liệu Text:")
            print(response.text[:500])
            return response.text
        
        # Nếu chưa biết, thử JSON trước
        else:
            try:
                data = response.json()
                print("\n✓ Dữ liệu JSON:")
                print(json.dumps(data[:100] if isinstance(data, list) else data, 
                               ensure_ascii=False, indent=2))
                return data
            except:
                # Thử CSV
                try:
                    df = pd.read_csv(StringIO(response.text))
                    print("\n✓ Dữ liệu CSV:")
                    print(df.head())
                    return df
                except:
                    print("\n✓ Dữ liệu (raw):")
                    print(response.text[:500])
                    return response.text
    
    except Exception as e:
        print(f"Lỗi khi phân tích dữ liệu: {e}")
        return None

def save_data(data, output_file='output.json'):
    """
    Lưu dữ liệu vào file
    """
    try:
        if isinstance(data, pd.DataFrame):
            output_file = output_file.replace('.json', '.csv')
            data.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"\n✓ Đã lưu dữ liệu vào: {output_file}")
        elif isinstance(data, dict) or isinstance(data, list):
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n✓ Đã lưu dữ liệu vào: {output_file}")
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(data))
            print(f"\n✓ Đã lưu dữ liệu vào: {output_file}")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu: {e}")

def main():
    # URL của dataset
    url = "https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/9CB7F264-50B3-4E67-9D29-D1A1054488B2/resource/45C57D8B-596B-480E-9D39-B7A608DC4D1B/download"
    
    # Tải dữ liệu
    response = download_data(url)
    
    if response:
        # Phân tích dữ liệu
        data = parse_data(response)
        
        # Lưu dữ liệu
        if data is not None:
            save_data(data)

if __name__ == "__main__":
    main()
