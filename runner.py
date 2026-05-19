import subprocess
import sys

print("Chạy chương trình...")
result = subprocess.run([sys.executable, "d:/11342629/excercise_04/fetch_data_readable.py"],
                       capture_output=False, text=True, timeout=120)
print(f"\nChương trình kết thúc với code: {result.returncode}")
