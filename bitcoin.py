#This is the code for showing crypto data in flask connected to index.html

from flask import Flask, render_template, request
import requests
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)


# Fetch cryptocurrency data
def fetch_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []


# Get price change for a specific cryptocurrency over the last n minutes
def get_price_change(crypto_id, minutes):
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=minutes)

    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/range?vs_currency=usd&from={start_time.timestamp()}&to={end_time.timestamp()}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search']
        crypto_data = fetch_crypto_data()
        filtered_data = [coin for coin in crypto_data if search_query.lower() in coin['name'].lower()]
    else:
        filtered_data = fetch_crypto_data()

    return render_template('index.html', coins=filtered_data)


if __name__ == '__main__':
    app.run(debug=True)
