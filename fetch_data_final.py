import requests
import pandas as pd
from io import BytesIO
import sys
from flask import Flask, render_template

# 設置 UTF-8 編碼用於 stdout (對 Windows 很重要)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 關閉 SSL 警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# API URL - 35 bản ghi dữ liệu
DATA_URL = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"

# Cache để lưu dữ liệu
_cached_data = None


def fetch_data_from_api():
    """Tải dữ liệu từ API"""
    try:
        print(f"🔄 Đang tải dữ liệu từ API...")
        response = requests.get(DATA_URL, timeout=30, verify=False)
        response.raise_for_status()
        
        # Parse CSV
        df = pd.read_csv(BytesIO(response.content), encoding='utf-8-sig')
        print(f"✓ Tải thành công! Tổng {len(df)} bản ghi\n")
        return df
    except Exception as e:
        print(f"❌ Lỗi khi tải dữ liệu: {e}")
        return None


def get_data():
    """Lấy dữ liệu (sử dụng cache hoặc tải mới)"""
    global _cached_data
    if _cached_data is None:
        _cached_data = fetch_data_from_api()
    return _cached_data


def dataframe_to_dict_list(data):
    """Chuyển DataFrame thành list of dictionaries để hiển thị"""
    if isinstance(data, pd.DataFrame):
        safe_df = data.where(pd.notnull(data), None)
        return safe_df.to_dict(orient='records')
    return []


@app.route('/')
def index():
    """Trang chủ - Hiển thị tất cả 35 bản ghi dữ liệu"""
    data = get_data()
    
    if data is None:
        return "<h1>❌ Lỗi: Không thể tải dữ liệu từ API</h1>", 500
    
    # Chuyển đổi dữ liệu
    total_records = len(data)
    columns = list(data.columns)
    rows = dataframe_to_dict_list(data)
    
    return render_template(
        'index.html',
        total_records=total_records,
        displayed_records=total_records,
        columns=columns,
        rows=rows,
        timestamp=pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    )


@app.route('/api/data')
def api_data():
    """API endpoint - Trả về JSON của tất cả dữ liệu"""
    data = get_data()
    if data is None:
        return {"error": "Không thể tải dữ liệu"}, 500
    
    return {
        "total_records": len(data),
        "columns": list(data.columns),
        "data": dataframe_to_dict_list(data)
    }


def start_server(host='127.0.0.1', port=5000):
    """Khởi động Flask server với auto-reload"""
    global _cached_data
    _cached_data = None  # Reset cache khi khởi động
    
    print(f"🚀 Flask server khởi động tại http://{host}:{port}/")
    print(f"📝 Chế độ DEBUG đã bật - Code thay đổi sẽ tự động reload")
    print(f"⏹️  Nhấn Ctrl+C để dừng server\n")
    
    try:
        app.run(host=host, port=port, debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print("\n\n✋ Server đã dừng.")


if __name__ == "__main__":
    start_server()
