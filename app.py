from flask import Flask, render_template
from fetch_data import fetch_records

app = Flask(__name__)


@app.route("/")
def index():
    # fetch first 35 records; keep verify_ssl=False to avoid cert issues in this env
    records = fetch_records(limit=35, verify_ssl=False)
    return render_template("index.html", records=records)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
