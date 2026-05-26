import requests
import csv
from io import StringIO

# URL API CSV
URL = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"

def fetch_records(limit: int = 35, verify_ssl: bool = False, timeout: int = 10):
    """Fetch CSV from the remote URL and return a list of dict records.

    Default `verify_ssl=False` to match prior behavior in this environment.
    """
    try:
        response = requests.get(URL, timeout=timeout, verify=verify_ssl)
        response.raise_for_status()
        csv_reader = csv.DictReader(StringIO(response.text))
        records = list(csv_reader)
        return records[:limit]
    except requests.exceptions.RequestException:
        raise


if __name__ == "__main__":
    try:
        records = fetch_records(limit=35, verify_ssl=False)
        for index, record in enumerate(records, start=1):
            print(f"\n{index}.")
            for key, value in record.items():
                print(f"  {key}: {value}")
        print(f"\n\nTổng cộng: {len(records)} bản ghi")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
    except Exception as e:
        print(f"Lỗi: {e}")
