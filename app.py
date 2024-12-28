from flask import Flask, jsonify, render_template
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def get_sp500_symbols():
    """Fetch the current S&P 500 stock symbols."""
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    return table['Symbol'].tolist()

def get_top_and_bottom_stocks():
    """Fetch the top 10 best and worst performers."""
    symbols = get_sp500_symbols()
    data = yf.download(tickers=symbols, period="2d", interval="1d", group_by="ticker")
    
    # Calculate percent change for each stock
    performance = {}
    for symbol in symbols:
        try:
            yesterday_close = data.loc[(symbol, slice(None)), 'Adj Close'].iloc[-2]
            today_close = data.loc[(symbol, slice(None)), 'Adj Close'].iloc[-1]
            change_percent = ((today_close - yesterday_close) / yesterday_close) * 100
            performance[symbol] = change_percent
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    # Sort and extract top/bottom 10 performers
    sorted_performance = sorted(performance.items(), key=lambda x: x[1], reverse=True)
    top_10 = sorted_performance[:10]
    bottom_10 = sorted_performance[-10:]
    
    return {
        "top_10": [{"symbol": symbol, "change": f"{change:.2f}%"} for symbol, change in top_10],
        "bottom_10": [{"symbol": symbol, "change": f"{change:.2f}%"} for symbol, change in bottom_10],
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
