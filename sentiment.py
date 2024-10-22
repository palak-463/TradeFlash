#This is the code for showing stock data in flask connected to stocks.html

import pandas as pd
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = 'T3DNBEKHNHX4L6BO.'

# Extended list of stock symbols and their corresponding company names
STOCKS = {
    "AAPL": "Apple Inc.",
    "GOOGL": "Alphabet Inc.",
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc.",
    "FB": "Meta Platforms Inc.",
    "NFLX": "Netflix Inc.",
    "NVDA": "NVIDIA Corporation",
    "JPM": "JPMorgan Chase & Co.",
    "V": "Visa Inc.",
    # Add more stocks as needed
}

def fetch_stock_data(stock_symbols):
    stock_data = {}
    for symbol in stock_symbols:
        try:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'
            response = requests.get(url)
            data = response.json()
            time_series = data.get('Time Series (5min)', {})
            if time_series:
                latest_time = sorted(time_series.keys())[0]
                latest_data = time_series[latest_time]
                stock_data[symbol] = {
                    "company": STOCKS[symbol],
                    "price": float(latest_data["4. close"]),
                    "change": (float(latest_data["4. close"]) - float(latest_data["1. open"])) / float(latest_data["1. open"]) * 100
                }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return stock_data

@app.route("/", methods=["GET", "POST"])
def index():
    filtered_data = []

    if request.method == "POST":
        search_query = request.form.get("search").upper()
        stocks_to_display = [stock for stock in STOCKS if search_query in stock]
    else:
        stocks_to_display = STOCKS.keys()

    data = fetch_stock_data(stocks_to_display)

    if data:
        for stock in data:
            filtered_data.append({
                "name": stock,
                "company": data[stock]["company"],
                "price": data[stock]["price"],
                "change": round(data[stock]['change'], 2)
            })

    return render_template('stocks.html', stocks=filtered_data)

if __name__ == "__main__":
    app.run(debug=True)
