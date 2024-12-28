from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "your_alpha_vantage_api_key"
STOCK_URL = "https://www.alphavantage.co/query"

def get_top_and_bottom_stocks():
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": "AAPL",  # Example; you can loop through symbols for more
        "apikey": API_KEY,
    }
    response = requests.get(STOCK_URL, params=params)
    data = response.json()

    # Simplified logic for demo (customize with your own sorting logic)
    return {
        "top_10": [{"name": "Stock A", "growth": "+10%"}],
        "bottom_10": [{"name": "Stock B", "growth": "-5%"}],
    }

@app.route("/api/stocks")
def stocks():
    data = get_top_and_bottom_stocks()
    return jsonify(data)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
