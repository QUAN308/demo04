import requests
import json
import pandas as pd
from io import StringIO, BytesIO
import os
import sys

# 設置 UTF-8 編碼用於 stdout (對 Windows 很重要)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 關閉 SSL 警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 導入用於打印漂亮表格的庫
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

def download_data(url):
    """從 URL 下載數據"""
    try:
        print(f"🔄 正在從以下位置下載數據: {url}")
        response = requests.get(url, timeout=30, verify=False)
        response.raise_for_status()
        print(f"✓ 成功! 狀態碼: {response.status_code}\n")
        return response
    except requests.exceptions.RequestException as e:
        print(f"❌ 下載數據錯誤: {e}")
        return None

def parse_data(response):
    """分析來自 response 的數據"""
    content_type = response.headers.get('content-type', '')
    
    try:
        if 'json' in content_type:
            return response.json()
        elif 'csv' in content_type or 'text' in content_type:
            # 使用 BytesIO 和 utf-8-sig 編碼 (處理 BOM)
            df = pd.read_csv(BytesIO(response.content), encoding='utf-8-sig')
            return df
        elif 'excel' in content_type or 'spreadsheet' in content_type:
            return pd.read_excel(BytesIO(response.content))
        else:
            try:
                return response.json()
            except:
                try:
                    df = pd.read_csv(BytesIO(response.content), encoding='utf-8-sig')
                    return df
                except:
                    return response.text
    except Exception as e:
        print(f"❌ 分析數據錯誤: {e}")
        return None

def print_table_beautiful(data):
    """直接在終端打印漂亮的表格"""
    if isinstance(data, pd.DataFrame):
        print("\n" + "╔" + "═" * 118 + "╗")
        print("║" + " " * 40 + "📊 來自 API 的數據" + " " * 62 + "║")
        print("╚" + "═" * 118 + "╝\n")
        
        print(f"📍 信息:")
        print(f"   • 總行數: {len(data)}")
        print(f"   • 總列數: {len(data.columns)}")
        print(f"   • 加載日期: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
        print("📋 數據詳情 (顯示前 5 筆記錄):\n")
        
        # 以列表形式顯示 key: value
        for idx, (_, row) in enumerate(data.head(5).iterrows()):
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"📌 記錄 #{idx + 1}:")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            for col, value in row.items():
                # 格式化值
                if pd.isna(value):
                    value_str = "(空)"
                elif len(str(value)) > 60:
                    value_str = str(value)[:57] + "..."
                else:
                    value_str = str(value)
                
                # 打印 key: value 對
                print(f"  • {col}: {value_str}")
            
            print()
        
        print("═" * 120 + "\n")

def save_as_table(data, output_file='output_table.txt'):
    """以漂亮的表格形式保存數據 (文本格式)"""
    if isinstance(data, pd.DataFrame):
        with open(output_file, 'w', encoding='utf-8') as f:
            # 標題
            f.write("=" * 100 + "\n\n")
            f.write("📊 從 API 下載的數據\n")
            f.write("=" * 100 + "\n\n")
            
            # 統計
            f.write(f"總行數: {len(data)}\n")
            f.write(f"總列數: {len(data.columns)}\n")
            f.write(f"列: {', '.join(data.columns)}\n\n")
            
            # 表格
            f.write(data.to_string(index=True))
            f.write("\n\n" + "=" * 100 + "\n")
        
        print(f"✓ 已將文本表格保存到: {output_file}")
        return output_file

def save_as_html(data, output_file='output_table.html'):
    """以 HTML 形式保存數據"""
    if isinstance(data, pd.DataFrame):
        html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dữ Liệu Từ API</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        .stat-box {{
            flex: 1;
            min-width: 150px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 24px;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 12px;
            margin-top: 5px;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background-color: #007bff;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #0056b3;
        }}
        td {{
            padding: 10px 12px;
            border: 1px solid #ddd;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f0f0f0;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 下載的 API 數據</h1>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{len(data)}</div>
                <div class="stat-label">總行數</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(data.columns)}</div>
                <div class="stat-label">總列數</div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    {"".join(f"<th>{col}</th>" for col in data.columns)}
                </tr>
            </thead>
            <tbody>
                {"".join(f"<tr><td style='background-color: #e8f4f8; font-weight: bold;'>{i+1}</td>" + 
                          "".join(f"<td>{val}</td>" for val in row) + "</tr>" 
                          for i, (_, row) in enumerate(data.iterrows()))}
            </tbody>
        </table>
        
        <div class="timestamp">
            創建於: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ 已將 HTML 保存到: {output_file}")
        return output_file

def save_as_markdown(data, output_file='output_table.md'):
    """以 Markdown 形式保存數據"""
    if isinstance(data, pd.DataFrame):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📊 下載的 API 數據\n\n")
            f.write(f"**總行數:** {len(data)}\n\n")
            f.write(f"**總列數:** {len(data.columns)}\n\n")
            f.write("## 數據\n\n")
            f.write(data.to_markdown(index=True))
            f.write("\n")
        
        print(f"✓ 已將 Markdown 保存到: {output_file}")
        return output_file

def save_as_pretty_text(data, output_file='output_pretty.txt'):
    """以漂亮的文本形式保存數據"""
    if isinstance(data, pd.DataFrame):
        try:
            from tabulate import tabulate
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("╔" + "═" * 98 + "╗\n")
                f.write("║" + " " * 30 + "📊 DỮ LIỆU TỪ API" + " " * 52 + "║\n")
                f.write("╚" + "═" * 98 + "╝\n\n")
                
                f.write(f"📍 Thông tin:\n")
                f.write(f"   • Tổng hàng (dòng): {len(data)}\n")
                f.write(f"   • Tổng cột: {len(data.columns)}\n")
                f.write(f"   • Ngày tải: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                
                f.write("📋 Chi tiết dữ liệu:\n\n")
                table_str = tabulate(data, headers="keys", tablefmt="grid", 
                                    showindex="always", maxcolwidths=20)
                f.write(table_str)
                f.write("\n\n" + "═" * 100 + "\n")
        except ImportError:
            # 如果沒有 tabulate，使用簡單格式
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("┌" + "─" * 98 + "┐\n")
                f.write("│" + " " * 30 + "📊 來自 API 的數據" + " " * 52 + "│\n")
                f.write("└" + "─" * 98 + "┘\n\n")
                
                f.write(f"📍 信息:\n")
                f.write(f"   • 總行數: {len(data)}\n")
                f.write(f"   • 總列數: {len(data.columns)}\n\n")
                
                f.write(data.to_string(index=True))
                f.write("\n\n" + "─" * 100 + "\n")
        
        print(f"✓ 已將漂亮文本保存到: {output_file}")
        return output_file

def main():
    url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"
    
    # 下載數據
    response = download_data(url)
    
    if response:
        # 分析數據
        data = parse_data(response)
        
        if data is not None:
            # 📌 直接在終端打印漂亮的表格
            print_table_beautiful(data)
            
            print("💾 正在以不同格式保存數據:\n")
            
            # 以不同格式保存
            save_as_pretty_text(data, 'output_pretty.txt')
            save_as_markdown(data, 'output_table.md')
            save_as_html(data, 'output_table.html')
            save_as_table(data, 'output_table.txt')
            
            print("\n✅ 完成! 已保存的文件:")
            print("   1. output_pretty.txt  - 帶 Unicode 邊框的漂亮表格")
            print("   2. output_table.txt   - 基本文本表格")
            print("   3. output_table.md    - Markdown 格式")
            print("   4. output_table.html  - HTML 網頁 (在瀏覽器中打開)")
            print("\n📌 建議: 查看下面的表格或在瀏覽器中打開 HTML 文件")

if __name__ == "__main__":
    main()
