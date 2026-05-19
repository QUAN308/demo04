# Program để tải dữ liệu từ API

## Mô tả
Chương trình này tải dữ liệu từ API của Bộ Nội vụ Đài Loan và tự động nhận dạng định dạng dữ liệu (JSON, CSV, Excel, v.v.)

## Cài đặt

### Bước 1: Cài đặt thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy chương trình
```bash
python fetch_data.py
```

## Tính năng

✓ Tải dữ liệu từ URL API  
✓ Tự động phát hiện định dạng (JSON, CSV, Excel, Text)  
✓ Hiển thị 50 dòng đầu tiên của dữ liệu  
✓ Xử lý lỗi HTTP và network  
✓ Lưu dữ liệu vào file (tự động chọn định dạng phù hợp)  

## Cách sử dụng

### Sử dụng mặc định
```bash
python fetch_data.py
```
Chương trình sẽ tự động tải dữ liệu từ URL được cấu hình sẵn.

### Chỉnh sửa URL
Mở file `fetch_data.py` và thay đổi URL trong hàm `main()`:
```python
url = "your_api_url_here"
```

### Sử dụng theo chương trình khác
```python
from fetch_data import download_data, parse_data, save_data

# Tải dữ liệu
response = download_data("https://your-api-url.com")

# Phân tích dữ liệu
data = parse_data(response)

# Lưu dữ liệu
save_data(data, "output.json")
```

## Output
- Hiển thị trên console: 50 hàng đầu tiên
- File được lưu: `output.json` (hoặc `output.csv` nếu là dữ liệu bảng)

## Hỗ trợ các định dạng
- JSON
- CSV
- Excel (.xlsx, .xls)
- Plain Text
- Tự động chuyển đổi giữa các định dạng

## Mã lỗi
Nếu gặp lỗi:
- **RequestException**: Kiểm tra URL và kết nối internet
- **JSONDecodeError**: Dữ liệu không phải là JSON hợp lệ
- **ParserError (CSV)**: Dữ liệu không phải là CSV hợp lệ

## Yêu cầu Python
Python 3.6 trở lên
